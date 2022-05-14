from .views import *

app_name = 'watchlist'
urlpatterns = [
    path('', login_required(views.WatchlistView.as_view()), name='watchlist'),
    ]
