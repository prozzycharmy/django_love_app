import random
import string
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Message, CustomUser, LinkType, UserLink, AnonymousMessage, MessagePhoto
from .forms import MessageForm, RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm, AnonymousMessageForm

def index(request):
    occasions = [
        "Valentine",
        "New Year",
        "Easter",
        "Christmas",
        "Birthday",
        "Anniversary",
        "Eid'l fitr",
        "Eid'l mubarak",
    ]
    return render(request, 'index.html',{"occasions":occasions})

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            
            # Handle extra photos
            extra_photos = request.FILES.getlist('extra_photos')
            for f in extra_photos:
                MessagePhoto.objects.create(message=msg, image=f)
                
            return redirect('preview_message', slug=msg.slug)
    else:
        form = MessageForm()
    return render(request, 'create.html', {'form': form})

def preview_message(request, slug):
    message = get_object_or_404(Message, slug=slug)
    return render(request, 'preview.html', {'message': message})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def forget_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                code = ''.join(random.choices(string.digits, k=6))
                user.reset_code = code
                user.reset_code_expiry = timezone.now() + timedelta(minutes=10)
                user.save()
                messages.info(request, f"Reset code sent to your email (Testing: {code})")
                request.session['reset_email'] = email
                return redirect('reset_password')
            except CustomUser.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
    else:
        form = ForgetPasswordForm()
    return render(request, 'forget_password.html', {'form': form})

def reset_password_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forget_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            reset_code = form.cleaned_data['reset_code']
            new_password = form.cleaned_data['new_password']
            try:
                user = CustomUser.objects.get(email=email, reset_code=reset_code)
                if user.reset_code_expiry > timezone.now():
                    user.set_password(new_password)
                    user.reset_code = None
                    user.reset_code_expiry = None
                    user.save()
                    messages.success(request, "Password reset successful. You can now login.")
                    del request.session['reset_email']
                    return redirect('login')
                else:
                    messages.error(request, "Reset code expired.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid reset code.")
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

@login_required
def dashboard(request):
    user_links = UserLink.objects.filter(user=request.user).order_by('-created_at')
    # Filter out link types that the user already has
    existing_type_ids = user_links.values_list('link_type_id', flat=True)
    available_link_types = LinkType.objects.exclude(id__in=existing_type_ids)
    
    # Get recent created messages (previews)
    recent_previews = Message.objects.filter(user=request.user).order_by('-date_created')[:5]
    
    return render(request, 'dashboard.html', {
        'user_links': user_links,
        'available_link_types': available_link_types,
        'recent_previews': recent_previews
    })

@login_required
def all_previews(request):
    previews = Message.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'all_previews.html', {'previews': previews})

@login_required
def create_link(request, link_type_id):
    link_type = get_object_or_404(LinkType, id=link_type_id)
    UserLink.objects.get_or_create(user=request.user, link_type=link_type)
    messages.success(request, f"Link for '{link_type.name}' created successfully!")
    return redirect('dashboard')

def send_anonymous_message(request, short_code):
    link = get_object_or_404(UserLink, short_code=short_code)
    if request.method == 'POST':
        form = AnonymousMessageForm(request.POST)
        if form.is_valid():
            anon_msg = form.save(commit=False)
            anon_msg.link = link
            anon_msg.save()
            messages.success(request, "Anonymous message sent successfully!")
            return render(request, 'message_sent.html', {'link': link})
    else:
        form = AnonymousMessageForm()
    return render(request, 'send_message.html', {'link': link, 'form': form})

@login_required
def received_messages(request, link_id):
    link = get_object_or_404(UserLink, id=link_id, user=request.user)
    received_msgs = link.received_messages.all().order_by('-created_at')
    return render(request, 'received_messages.html', {'link': link, 'messages': received_msgs})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(AnonymousMessage, id=message_id, link__user=request.user)
    message.is_read = True
    message.save()
    return render(request, 'message_detail.html', {'message': message})
