from django.urls import path
from . import views


urlpatterns = [
    path('start_here/', views.StartHereView.as_view(), name='start_here'),
    path('community/', views.community, name='community'),
    path('learning-paths/', views.community, name='community'),
    path('tutorials/all/', views.community, name='community'),
    path('office-hours/', views.community, name='community'),
    path('podcasts/rpp/', views.community, name='community'),
    path('products/', views.community, name='community'),
    path('products/books/', views.community, name='community'),
    path('account/join/', views.community, name='community'),
    path('newsletter/', views.community, name='community'),
    path('team/', views.community, name='community'),
    path('write-for-us/', views.community, name='community'),
    path('become-an-instructor/', views.community, name='community'),

]
