
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('markets/', include('markets.urls'), name='markets'),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('trade/', include('trade.urls'), name='trade'),
    path('watchlist/', include('watchlist.urls'), name='watchlist'),
    path('portfolio/', include('portfolio.urls'), name='portfolio'),
    path('trends/', include('trends.urls'), name='trends'),
    path('news/', include('news.urls'), name='news'),
    path('calendar/', include('_calendar.urls'), name='calendar'),
    path('data/', include('data.urls'), name='data'),
    path('messenger/', include('messenger.urls'), name='messenger'),
    path('', include('website.urls'), name='website'),
]


