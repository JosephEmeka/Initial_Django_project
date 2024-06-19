from django.urls import path
from . import views

urlpatterns = [
    path('welcome', views.say_hello),
    path('hello/<str:name>/', views.welcome),
]
# python manage.py runserver
# python manage.py runserver 8001
