from django.shortcuts import render, redirect, get_object_or_404
from.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pyotp
from .models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from gamerz.models import OngoingGame, Reservation
from datetime import datetime, timedelta
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)
def send_otp(request):
    # Check if 'otp_secret_key' already exists in session
    if 'otp_secret_key' not in request.session:
        secret_key = pyotp.random_base32()
        request.session['otp_secret_key'] = secret_key
    else:
        secret_key = request.session['otp_secret_key']
    
    totp = pyotp.TOTP(secret_key, interval=300)  # Interval set to 5 minutes
    otp = totp.now()
    
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    # Get the user's email from the session
    username = request.session.get('username')
    if not username:
        messages.error(request, 'Session expired or invalid. Please log in again.')
        return redirect('login')

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(username=username)
        email = user.email
    except UserModel.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('login')

    # Prepare and send the OTP email
    subject = 'Your OTP Code'
    message = f'Your one-time-password (OTP) is {otp}. It is valid for 5 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, email_from, recipient_list)
        logger.info(f'OTP sent to {email}: {otp}')
    except Exception as e:
        logger.error(f'Failed to send OTP email to {email}: {e}')
        messages.error(request, 'Failed to send OTP email. Please try again.')
        return redirect('login')


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
        otp_input = request.POST.get('otp')
        username = request.session.get('username')

        if not username:
            messages.error(request, 'Session expired or invalid. Please log in again.')
            return redirect('login')

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if datetime.now() <= valid_until:
                totp = pyotp.TOTP(otp_secret_key, interval=300)  # Ensure interval matches
                if totp.verify(otp_input):
                    # Retrieve the user instance
                    UserModel = get_user_model()
                    try:
                        user = UserModel.objects.get(username=username)
                        logger.info(f'User {username} authenticated successfully with OTP.')
                    except UserModel.DoesNotExist:
                        messages.error(request, 'User not found')
                        logger.error(f'User {username} not found during OTP verification.')
                        return redirect('login')

                    # Log in the user
                    login(request, user)

                    # Clean up session data
                    request.session.pop('otp_secret_key', None)
                    request.session.pop('otp_valid_date', None)

                    # Redirect based on role
                    if user.role == 'ADMIN':
                        return redirect('admin')
                    elif user.role == 'EMPLOYEE':
                        return redirect('employee')
                    else:
                        return redirect('gamerz')
                else:
                    messages.error(request, 'Invalid OTP')
                    logger.warning(f'Invalid OTP entered by user {username}.')
            else:
                messages.error(request, 'OTP has expired')
                logger.warning(f'OTP for user {username} has expired.')
        else:
            messages.error(request, 'Oops, something went wrong')
            logger.error(f'OTP session data missing for user {username}.')

    return render(request, 'users/otp.html')


def admin_dashboard_view(request):
    return render(request, 'users/admin.html')


def employee_dashboard_view(request):

    today = timezone.now().date()

    # Calculate dynamic data
    active_gamers_count = OngoingGame.objects.filter(status='Active').count()
    reservations_today_count = Reservation.objects.filter(start_time__date=today).count()
    games_in_progress_count = OngoingGame.objects.filter(status__in=['Active', 'Paused']).count()
    
    gamers_activity = []
    now = timezone.now()
    ongoing_games = OngoingGame.objects.select_related('user', 'station').all()

    for game in ongoing_games:
        playtime_minutes = int((now - game.start_time).total_seconds() / 60)
        gamers_activity.append({
            'gamer_id': game.user.id,
            'username': game.user.username,
            'game_title': game.game_title,
            'playtime': playtime_minutes,
            'status': game.status,
        })

    context = {
        'active_gamers_count': active_gamers_count,
        'reservations_today_count': reservations_today_count,
        'games_in_progress_count': games_in_progress_count,
        'gamers_activity': gamers_activity,
    }

    return render(request, 'users/employee.html', context)



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
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role', 'GAMER')  # Default to 'GAMER' if no role is provided
            user.save()

            # Store the username in session
            request.session['username'] = user.username
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                print(request, error)
    form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request):
    return render(request, 'users/profile.html')

