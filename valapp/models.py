
import random
import string
import uuid
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the user's full name, or email if no name set."""
        full = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full if full else self.email

    def get_short_name(self):
        """Return the short name for the user (first name or email)."""
        return self.first_name or self.email

class Message(models.Model):
    OCCASIONS = [
        ('Valentine', 'Valentine'),
        ('New Year', 'New Year'),
        ('Easter', 'Easter'),
        ('Christmas', 'Christmas'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ("Eid'l fitr","Eid'l fitr"),
        ("Eid'l mubarak","Eid'l mubarak"),
    ]

    THEMES = [
        ('Romantic', 'Romantic'),
        ('Friendly', 'Friendly'),
        ('Family', 'Family'),
        ('Elegant', 'Elegant'),
    ]

    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_messages')
    occasion = models.CharField(max_length=20, choices=OCCASIONS)
    theme = models.CharField(max_length=20, choices=THEMES)
    message = models.TextField()
    photo = models.ImageField(upload_to='messages/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            sender_part = slugify(self.sender)[:3]
            recipient_part = slugify(self.recipient)[:3]
            base_slug = f"{sender_part}-{recipient_part}"

            slug = base_slug
            counter = 1

            while Message.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.sender} → {self.recipient}"

class MessagePhoto(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='messages/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.message.slug}"

class LinkType(models.Model):
    name = models.CharField(max_length=100) # e.g., "Ask me anything"
    prompt = models.CharField(max_length=255) # e.g., "Send me a secret message!"
    icon = models.CharField(max_length=50, default='💌')
    color_gradient = models.CharField(max_length=255, default='linear-gradient(135deg, #f45a75, #ff738d)')

    def __str__(self):
        return self.name

class UserLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='links')
    link_type = models.ForeignKey(LinkType, on_delete=models.CASCADE)
    short_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            # Get first 3 letters of email or name
            prefix = slugify(self.user.get_short_name())[:3]
            if not prefix:
                prefix = "usr"
            
            # Generate random string according to user's request
            while True:
                # Randomly pick a digit to satisfy "and number"
                random_digit = random.choice(string.digits)
                # Randomly pick 7 more chars for the first block
                part1_random = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
                # Randomly pick 6 more chars for the second block
                part2_random = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                
                # Combine them. 
                code = f"{prefix}{random_digit}{part1_random}-{part2_random}"
                
                if not UserLink.objects.filter(short_code=code).exists():
                    self.short_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.link_type.name} ({self.short_code})"

class AnonymousMessage(models.Model):
    link = models.ForeignKey(UserLink, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.link.user.email} from {self.created_at}"
