from django.urls import path
from. import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('otp/', views.otp_view, name='otp'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('admindashboard/', views.admin_dashboard_view, name='admin'),
    path('employeedashboard/', views.employee_dashboard_view, name='employee'),
    #path('gamerdashboard/', views.gamer_dashboard_view, name='gamer'),
    path('user/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('user/delete/<int:user_id>/', views.delete_user, name='user_delete'),
    path('adminregisteruser/', views.admin_register_user_view, name='adminregisteruser'),
]