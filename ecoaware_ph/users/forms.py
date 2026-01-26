# users/forms.py

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms 
from .models import User as CustomUser  # make sure this points to your custom user model

# Tailwind styling for inputs
TAILWIND_INPUT_CLASS = 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500'


# ------------------------
# LOGIN FORM
# ------------------------
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': TAILWIND_INPUT_CLASS})
    )


# ------------------------
# REGISTRATION FORM
# ------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        self.fields['username'].help_text = None
        if 'password' in self.fields:
             self.fields['password'].help_text = None # Just in case
        
        # Also styling
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = TAILWIND_INPUT_CLASS




class CustomUserChangeForm(UserChangeForm):
    password = None  # hide the password field
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'first_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT_CLASS}),
        }
