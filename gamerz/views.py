from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
from.credentials import *
from django.http import JsonResponse
from django.contrib import messages
import stripe
from django.urls import reverse

def gamerz_view(request):
    return render(request, 'gamerz/gamer.html')

@login_required
def game_list_view(request):
    games = Game.objects.all()
    return render(request, 'gamerz/game_list.html', {'games': games})

def game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'gamerz/game_detail.html', {'game': game})

def favorite_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    if game in user.favorite_games.all():
        user.favorite_games.remove(game)
    else:
        user.favorite_games.add(game)
    return redirect('game_detail', game_id=game_id)

@login_required
def favorite_games_list_view(request):
    user = request.user
    favorite_games = user.favorite_games.all()
    return render(request, 'gamerz/favorite_games_list.html', {'favorite_games': favorite_games})



def add_favorite(request, pk):
    game = get_object_or_404(Game, pk=pk)
    request.user.favorite_games.add(game)
    return redirect('game_list')

def remove_favorite(request, pk):
    game = get_object_or_404(Game, pk=pk)
    request.user.favorite_games.remove(game)
    return redirect('game_list')

def game_reservations(request):
    # Implement game reservations view here
    pass

def leaderboards(request):
    # Implement leaderboards view here
    pass

def gameform(request):
    return render(request, 'gamerz/game_form.html')


def reservation_view(request):
    stations = GamingStation.objects.all()
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration'))
        end_time = datetime.fromisoformat(start_time) + timedelta(hours=duration)
        station = GamingStation.objects.get(id=station_id)
        reservation = Reservation(
            user=request.user,
            station=station,
            start_time=start_time,
            end_time=end_time,
        )
        reservation.save()
        return redirect('payments', reservation_id=reservation.id)
    return render(request, 'gamerz/reservation.html', {'stations': stations})


def reservation_list_view(request):
    reservations = Reservation.objects.filter(user=request.user)
    reservation_data = []

    for reservation in reservations:
        # Calculate the total hours
        total_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
        # Calculate the total cost
        total_cost = total_hours * 200  # Ksh 200 per hour

        # Store the data in a dictionary
        reservation_data.append({
            'station_name': reservation.station.name,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time,
            'total_hours': total_hours,
            'total_cost': total_cost
        })

    return render(request, 'gamerz/reservation_list.html', {'reservation_data': reservation_data})


def leaderboard_view(request):
    scores = GamerScore.objects.order_by('-score')[:10]
    return render(request, 'gamerz/leaderboard.html', {'scores': scores})

def achievement_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    achievements = Achievement.objects.filter(game=game)
    return render(request, 'gamerz/achievement.html', {'game': game, 'achievements': achievements})


def chat_room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    return render(request, 'chat/chat_room.html', {'room': room})

def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = room.messages.order_by('-timestamp')[:50]  # Get the last 50 messages
    messages = reversed(messages)  # Reverse them to show the most recent at the bottom
    return JsonResponse([{'user': message.user.username, 'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for message in messages], safe=False)

@csrf_exempt
def send_message(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, id=room_id)
        content = request.POST.get('content')
        message = Message.objects.create(room=room, user=request.user, content=content)
        return JsonResponse({'user': message.user.username, 'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')})


def shop_location_view(request):
    return render(request, 'gamerz/shop_location.html')


def payments_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'gamerz/payments.html', {'reservation': reservation})

def mpesa_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # Calculate the total hours and cost for the reservation
    total_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    total_cost = total_hours * 200  # Ksh 200 per hour

    reservation_data = {
        'station_name': reservation.station.name,
        'start_time': reservation.start_time,
        'end_time': reservation.end_time,
        'total_hours': total_hours,
        'total_cost': total_cost
    }

    if request.method == 'POST':
        phone = request.POST['phone']
        amount = total_cost
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        payment_request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "Gaming Station Reservation"
        }

        response = requests.post(api_url, json=payment_request, headers=headers)
        
        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 200:
            # Payment initiated successfully
            messages.success(request, "Payment initiated successfully. Please complete your payment via Mpesa.")
            return redirect('reservation_list')
        else:
            # Handle payment failure or errors here
            messages.error(request, f"Payment initiation failed. Error: {response.text}")
            return redirect('home')

    return render(request, 'gamerz/mpesa.html', {'reservation_data': reservation_data})



def paypal_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # Calculate the total hours and cost for the reservation
    total_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    total_cost = total_hours * 200  # Ksh 200 per hour

    reservation_data = {
        'station_name': reservation.station.name,
        'start_time': reservation.start_time,
        'end_time': reservation.end_time,
        'total_hours': total_hours,
        'total_cost': total_cost
    }

    if request.method == 'POST':
        
        return redirect('home')

    return render(request, 'gamerz/paypal.html', {'reservation_data': reservation_data})



def payment_success(request):
    if request.method == 'POST':
        # Handle any necessary logic here
        messages.success(request, "Payment completed successfully!")
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)



def stripe_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # Calculate the total hours and cost for the reservation
    total_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    total_cost = total_hours * 200  # Ksh 200 per hour

    reservation_data = {
        'station_name': reservation.station.name,
        'start_time': reservation.start_time,
        'end_time': reservation.end_time,
        'total_hours': total_hours,
        'total_cost': total_cost,
        'reservation': reservation,  # Pass the reservation object
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'gamerz/stripe.html', {'reservation_data': reservation_data})


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    total_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    total_cost = int(total_hours * 200)  # Convert to integer (Ksh 200 per hour)
    
    print("Creating Stripe Checkout Session...")
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # Stripe expects currency in lowercase
                'product_data': {
                    'name': f'Reservation for {reservation.station.name}',
                },
                'unit_amount': total_cost * 100,  # Stripe expects amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('reservation_success')),
        cancel_url=request.build_absolute_uri(reverse('reservation_cancel')),
    )

    print("Stripe Checkout Session created:", session.id)
    
    return JsonResponse({
        'id': session.id
    })


def reservation_success(request):
    messages.success(request, "Payment completed successfully!")
    return render(request, 'gamerz/reservation_success.html')

def reservation_cancel(request):
    messages.error(request, "Payment was canceled.")
    return render(request, 'gamerz/reservation_cancel.html')


def event_list(request):
    events = Event.objects.filter(status='Scheduled').order_by('start_date')
    return render(request, 'gamerz/event_list.html', {'events': events})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Registration.objects.filter(event=event, user=request.user).exists():
        # User already registered
        return redirect('event_list')
    
    if event.max_participants and Registration.objects.filter(event=event).count() >= event.max_participants:
        # Event is full
        return redirect('event_list')

    registration = Registration.objects.create(event=event, user=request.user, status='Registered')
    return redirect('event_list')

@login_required
def my_events(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'gamerz/my_events.html', {'registrations': registrations})



def event_calendar(request):
    events = Event.objects.filter(status='Scheduled')
    return render(request, 'gamerz/event_calendar.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})



