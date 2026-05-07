from django.urls import path
from accounts import views


urlpatterns = [
  path('', views.home, name='home'),
  path('feed/', views.feed, name='feed'),
  path('register/', views.register_view, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('toggle-status/', views.toggle_status, name='toggle_status'),
  path('interests/', views.update_interests, name='update_interests'),
]