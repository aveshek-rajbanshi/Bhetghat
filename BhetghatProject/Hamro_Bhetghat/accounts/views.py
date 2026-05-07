from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.forms import RegisterForm
from accounts.models import UserProfile


def home(request):
  return render(request, 'home.html')


@login_required
def feed(request):
    # All profiles that are currently free — exclude yourself
    free_profiles = UserProfile.objects.filter(is_free=True).exclude(user=request.user).select_related('user') # efficient — fetches user in one query
    my_profile = request.user.profile
    
    context = {
               'free_profiles': free_profiles,
               'my_profile': my_profile,
               'free_count': free_profiles.count(),
             }
    return render(request, 'feed.html', context)




@login_required
@require_POST
def toggle_status(request):
    profile = request.user.profile
    profile.is_free = not profile.is_free   #flip T-F or F-T
    profile.save()
    return redirect('feed')


INTEREST_CHOICES = ['chai', 'futsal', 'gaming', 'study', 'movie','hiking']

@login_required
def update_interests(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        # request.POST.getlist() reads multiple checkbox values
        selected = request.POST.getlist('interests')
        # Only keep valid choices — ignore any injected values
        valid = [i for i in selected if i in INTEREST_CHOICES]
        profile.interests = ','.join(valid)
        profile.save()
        messages.success(request, 'Interests updated! ✅')
        return redirect('feed')
    
    current = profile.get_interest_list()
    context = {
                'interest_choices': INTEREST_CHOICES,
                'current_interests': current,
            }
        
    return render(request, 'interests.html', context)





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
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Loggin Successfully 🎉!!')
            
            # Go to the page they were trying to visit, or home
            next_url = request.GET.get('next', 'home')
            print(next_url)
            return redirect(next_url)
    else:
        # messages.error(request, f'Invalid username or password. Please try again.')
        return render(request, 'login.html', )




def logout_view(request):
    if request.method == 'POST': # logout should always be POST
       logout(request)
       messages.info(request, f'You have been logged out. See you soon!👋')
       return redirect('login')
     
    return redirect('home') # ignore GET requests to logout URL
