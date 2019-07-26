from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.FirstTrail.as_view()),
]