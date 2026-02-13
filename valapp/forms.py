from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'occasion', 'theme', 'message']
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'lux-input w-full px-5 py-4 rounded-xl',
                'placeholder': 'Your name'
            }),
            'recipient': forms.TextInput(attrs={
                'class': 'lux-input w-full px-5 py-4 rounded-xl',
                'placeholder': "Recipient's name"
            }),
            'occasion': forms.Select(attrs={
                'class': 'lux-input w-full px-5 py-4 rounded-xl bg-transparent'
            }),
            'theme': forms.Select(attrs={
                'class': 'lux-input w-full px-5 py-4 rounded-xl bg-transparent'
            }),
            'message': forms.Textarea(attrs={
                'class': 'lux-input w-full px-5 py-4 rounded-xl resize-none',
                'rows': 6,
                'placeholder': 'Write something unforgettable...'
            }),
        }
