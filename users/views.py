from django.shortcuts import render, redirect, get_object_or_404
from.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
import pyotp
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    # Get the user's email from the session
    username = request.session.get('username')
    User = get_user_model()

    try:
        user = User.objects.get(username=username)
        email = user.email
    except User.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('login')

    # Prepare and send the OTP email
    subject = 'Your OTP Code'
    message = f'Your one-time-password (OTP) is {otp}. Its valid for 2 minute'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        username = request.POST['username'] 
        password = request.POST['password'] 
        
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                send_otp(request)  # Send OTP and prepare for OTP verification
                request.session['username'] = username
                return redirect('otp')
            else:
                messages.error(request, "Invalid username or password")
        
        # Handling form errors
        for error in list(form.errors.values()):
            messages.error(request, error)
    
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def otp_view(request):
    if request.method == "POST":
        otp = request.POST['otp']
        username = request.session.get('username')

        # Debugging: Check what is stored in the session
        print(f"Username from session: {username}")

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    # Retrieve the user instance
                    User = get_user_model()
                    try:
                        user = User.objects.get(username=username)
                        # Debugging: Confirm user was found
                        print(f"Found user: {user}")
                    except User.DoesNotExist:
                        messages.error(request, 'User not found')
                        return redirect('login')

                    # Log in the user
                    login(request, user)

                    # Clean up session data
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('home')
                else:
                    messages.error(request, 'Invalid OTP')
            else:
                messages.error(request, 'OTP has expired')
        else:
            messages.error(request, 'Oops, something went wrong')
    
    return render(request, 'users/otp.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You are logout')
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                print(request, error)
    form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request):
    return render(request, 'users/profile.html')

