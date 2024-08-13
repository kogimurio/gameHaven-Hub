from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required


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