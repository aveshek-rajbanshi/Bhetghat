from django.urls import path
from accounts import views


urlpatterns = [
  path('', views.home, name='home'),
  path('feed/', views.feed, name='feed'),
  path('register/', views.register_view, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),

]