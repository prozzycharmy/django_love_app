
# Create your models here.
from django.db import models
from django.utils.text import slugify

class Message(models.Model):
    OCCASIONS = [
        ('Valentine', 'Valentine'),
        ('New Year', 'New Year'),
        ('Easter', 'Easter'),
        ('Christmas', 'Christmas'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
    ]

    THEMES = [
        ('Romantic', 'Romantic'),
        ('Friendly', 'Friendly'),
        ('Family', 'Family'),
        ('Elegant', 'Elegant'),
    ]

    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    occasion = models.CharField(max_length=20, choices=OCCASIONS)
    theme = models.CharField(max_length=20, choices=THEMES)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)  # added slug field

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
        return f"{self.sender_name} → {self.recipient_name}"
