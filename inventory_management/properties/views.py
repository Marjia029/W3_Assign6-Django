from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import CustomUserCreationForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.is_active = False  # Set the user to inactive
            user.save()
            # Add user to the "Property Owner" group
            group = Group.objects.get(name='Property Owners')
            user.groups.add(group)
            user.save()
            messages.success(request, 'Your account has been created successfully. Wait for admin activation.')
            return redirect('login')
        else:
            messages.error(request, 'Error during sign-up. Please try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')  # Or wherever you want to redirect after login
            else:
                messages.error(request, 'Your account is not activated yet. Please wait for admin approval.')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    
    return render(request, 'login.html')
