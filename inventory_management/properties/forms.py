from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Tailwind classes to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your username'
        })
        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter your email'
            })
        )
        self.fields['password1'].widget.attrs.update({
            'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirm your password'
        })

        # Customize help text
        for field_name, field in self.fields.items():
            if field.help_text:  # If help text exists
                field.help_text = f'<small class="text-gray-500 text-sm">{field.help_text}</small>'

        # Update field labels
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
