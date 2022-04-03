
from django.urls import path
from . import views

app_name = 'trends'
urlpatterns = [
    path('trends/', views.TrendsView.as_view(), name='trends'),
    path('twitter/', views.TwitterView.as_view(), name='twitter'),
    path('google/', views.GoogleView.as_view(), name='google'),
    path('reddit/', views.RedditView.as_view(), name='reddit'),

    ]
