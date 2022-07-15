from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
#builtin user model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#built in user model form
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

#Login page view
def loginPage(request):
    page= 'login'

    #check if user is authenticated
    if request.user.is_authenticated:
        return redirect('home')

    #handle errors and authenticate user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context ={'page': page}
    return render(request, 'base/login_register.html', context)

#Logout view
def logoutUser(request):
    logout(request)
    return redirect('home')


#Register page view
def registerPage(request):
    page ='register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.userame.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration failed')

    context ={'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

#Home page view with login required decorator
@login_required(login_url='login')
def home(request):

    return render(request, 'base/home.html')
