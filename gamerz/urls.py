from django.urls import path
from. import views


urlpatterns = [
    path('gamerz/', views.gamerz_view, name='gamerz'),
    path('games/', views.game_list_view, name='game_list'),
    path('games/<int:pk>/', views.game_detail_view, name='game_detail'),
    path('favorites/add/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),
    path('reservations/', views.game_reservations, name='game_reservations'),
    path('leaderboards/', views.leaderboards, name='leaderboards'),
    path('favoritegame/', views.favorite_game_view, name='favorite_game'),
]