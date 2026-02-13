from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm

def index(request):
    occasions = [
        "Valentine",
        "New Year",
        "Easter",
        "Christmas",
        "Birthday",
        "Anniversary",
    ]
    return render(request, 'index.html',{"occasions":occasions})

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save()
            return redirect('preview_message', slug=msg.slug)
    else:
        form = MessageForm()
    return render(request, 'create.html', {'form': form})

def preview_message(request, slug):
    message = get_object_or_404(Message, slug=slug)
    return render(request, 'preview.html', {'message': message})
