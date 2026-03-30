from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Message, CustomUser, AnonymousMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'occasion', 'theme', 'message', 'photo']
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'lux-input',
                'placeholder': 'Your name'
            }),
            'recipient': forms.TextInput(attrs={
                'class': 'lux-input',
                'placeholder': "Recipient's name"
            }),
            'occasion': forms.Select(attrs={
                'class': 'lux-input'
            }),
            'theme': forms.Select(attrs={
                'class': 'lux-input'
            }),
            'message': forms.Textarea(attrs={
                'class': 'lux-input',
                'rows': 6,
                'placeholder': 'Write something unforgettable...'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'lux-input',
                'accept': 'image/*'
            }),
        }

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'lux-input',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'lux-input',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'lux-input',
                'placeholder': 'Last name'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Password'
    }))

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Email'
    }))

class ResetPasswordForm(forms.Form):
    reset_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Reset Code'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'lux-input',
        'placeholder': 'New Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'lux-input',
        'placeholder': 'Confirm New Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class AnonymousMessageForm(forms.ModelForm):
    class Meta:
        model = AnonymousMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'lux-input',
                'rows': 5,
                'placeholder': 'Type your anonymous message here...'
            }),
        }
