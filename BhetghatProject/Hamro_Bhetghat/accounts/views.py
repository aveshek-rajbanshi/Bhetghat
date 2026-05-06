from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.forms import RegisterForm



def home(request):
  return render(request, 'home.html')


@login_required 
def feed(request):
    return render(request, 'feed.html')




def register_view(request):
    if request.user.is_authenticated:
       return redirect('home')
    
    if request.method == 'POST':
       form = RegisterForm(request.POST)
       
       if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Create the user
            user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
            
            # Auto-login after register
            # login(request, user)
            
            # messages.success(request, f'Welcome to Hamro Bhetghat, {username}! 👋')
            
            return redirect('login')
    
    else:
      
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})
      
      
      
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
      
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
          login(request, user)
          messages.success(request, f'Welcome back, {user.username}!👋')
          
          # Go to the page they were trying to visit, or home
          next_url = request.GET.get('next', 'home')
          return redirect(next_url)
    else:
        # messages.error(request, f'Invalid username or password. Please try again.')
        return render(request, 'login.html')




def logout_view(request):
    if request.method == 'POST': # logout should always be POST
       logout(request)
       messages.info(request, 'You have been logged out. See you soon!👋')
       return redirect('login')
     
    return redirect('home') # ignore GET requests to logout URL
