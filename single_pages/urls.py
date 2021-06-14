from django.urls import path
from . import views

urlpatterns = [
    path('about_developer/', views.about_developer),
    path('', views.landing),
]
