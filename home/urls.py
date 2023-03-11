from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('details/<int:tut_id>/<tut_slug>/', views.DetailView.as_view(), name='details'),
    path('delete/<int:tut_id>/', views.DeleteView.as_view(), name='delete'),
    path('update/<int:tut_id>/', views.UpdateView.as_view(), name='update'),
    path('create/<page_no>/', views.CreateView.as_view(), name='create'),
    path('reply/<int:tut_id>/<int:comment_id>/', views.TutorialAddReplyView.as_view(), name='add_reply'),
    path('search/', views.TutorialSearchView.as_view(), name='search'),
    path('articles/<int:art_id>/<str:slog>/', views.MongardArt),
    path('articles/<str:slog>/', views.roocketArt),
]
