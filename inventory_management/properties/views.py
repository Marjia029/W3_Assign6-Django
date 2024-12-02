from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

User = get_user_model()


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'  # Specify the template to render


class SignupView(CreateView):
    model = User  # Use the User model for the form
    form_class = CustomUserCreationForm  # Use your custom user creation form
    template_name = 'signup.html'  # The template to render the form
    success_url = reverse_lazy('login')  # Redirect to login page on success

    def form_valid(self, form):
        # Process the valid form data
        user = form.save(commit=False)
        user.is_active = False  # Set the user to inactive
        user.save()

        # Add the user to the "Property Owners" group
        try:
            group = Group.objects.get(name='Property Owners')
            user.groups.add(group)
        except Group.DoesNotExist:
            messages.error(self.request, 'Property Owners group does not exist. Please contact admin.')

        # Add a success message
        messages.success(self.request, 'Your account has been created successfully. Wait for admin activation.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Handle invalid form submissions
        messages.error(self.request, 'Error during sign-up. Please try again.')
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'login.html'  # Template for rendering the login page
    form_class = AuthenticationForm  # Use Django's built-in authentication form
    success_url = reverse_lazy('index')  # Redirect URL after successful login

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        Override it to add custom authentication logic.
        """
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, f'Welcome back, {user.username}!')
                return super().form_valid(form)
            else:
                messages.error(self.request, 'Your account is not activated yet. Please wait for admin approval.')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Invalid login credentials. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Handle the case where the form is invalid.
        """
        messages.error(self.request, 'Invalid login attempt. Please correct the errors and try again.')
        return super().form_invalid(form)