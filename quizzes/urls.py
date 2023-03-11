from django.urls import path
from . import views


urlpatterns = [
    path('quizzes/', views.quizzes, name='quizzes'),
    path('optins/process/', views.process, name='process'),
]
