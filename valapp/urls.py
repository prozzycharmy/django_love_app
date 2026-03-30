from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_message, name='create_message'),
    path('preview/<slug:slug>/', views.preview_message, name='preview_message'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/previews/', views.all_previews, name='all_previews'),
    path('create-link/<int:link_type_id>/', views.create_link, name='create_link'),
    path('pro/<str:short_code>/', views.send_anonymous_message, name='send_anonymous_message'),
    path('messages/<int:link_id>/', views.received_messages, name='received_messages'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
]
