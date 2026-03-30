from django.contrib import admin
from .models import CustomUser, Message, LinkType, UserLink, AnonymousMessage

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'occasion', 'theme', 'date_created')
    prepopulated_fields = {'slug': ('sender', 'recipient')}
    search_fields = ('sender', 'recipient', 'message')
    list_filter = ('occasion', 'theme')

@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'prompt')
    search_fields = ('name', 'prompt')

@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'link_type', 'short_code', 'created_at')
    search_fields = ('user__email', 'short_code')
    list_filter = ('link_type', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(AnonymousMessage)
class AnonymousMessageAdmin(admin.ModelAdmin):
    list_display = ('link', 'content_excerpt', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'link__link_type')
    search_fields = ('content', 'link__user__email')
    readonly_fields = ('created_at',)

    def content_excerpt(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_excerpt.short_description = 'Content'
