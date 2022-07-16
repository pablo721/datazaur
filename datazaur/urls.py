
from django.contrib import admin
from django.urls import path, include
from watchlist.views import PortfolioView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls'), name='website'),
    path('markets/', include('markets.urls'), name='markets'),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('trade/', include('trade.urls'), name='trade'),
    path('watchlist/', include('watchlist.urls'), name='watchlist'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('news/', include('news.urls'), name='news'),
    path('calendar/', include('_calendar.urls'), name='calendar'),
    path('trends/', include('trends.urls'), name='trends'),
    path('data/', include('data.urls'), name='data'),

]


