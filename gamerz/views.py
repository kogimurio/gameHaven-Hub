from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        end_time = request.POST.get('end_time')
        station = GamingStation.objects.get(id=station_id)
        reservation = Reservation(
            user=request.user, 
            station=station, 
            start_time=start_time, 
            end_time=end_time
        )
        reservation.save()
        return redirect('reservation_list')
    return render(request, 'gamerz/reservation.html', {'stations': stations})


def reservation_list_view(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'gamerz/reservation_list.html', {'reservations': reservations})


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



