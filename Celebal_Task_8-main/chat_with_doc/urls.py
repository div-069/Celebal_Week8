from django.contrib import admin
from django.urls import path, include
from .views import document_chat_view

urlpatterns = [
    path('', document_chat_view, name="document_chat"),
]