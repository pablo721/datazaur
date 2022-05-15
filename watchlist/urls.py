from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'watchlist'
urlpatterns = [
    path('', login_required(WatchlistView.as_view()), name='watchlist'),
    ]
