from django.contrib import admin
from django.urls import path
from django.urls import path, include
from scraper import views
urlpatterns = [
    path('', views.scrape,name='scrape'),
    path('delete', views.clear, name='clear'),
]
