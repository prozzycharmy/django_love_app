from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_message, name='create_message'),
    path('preview/<slug:slug>/', views.preview_message, name='preview_message'),
]
