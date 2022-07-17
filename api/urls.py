from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'crypto', views.CryptoView, basename='crypto')
# router.register(r'watchlist', views.WatchlistView)
# router.register(r'portfolio', views.PortfolioView)
# router.register(r'fx', views.CurrencyView)
# router.register(r'commodity', views.CommodityView)
# router.register(r'country', views.CountryView)
# router.register(r'ticker', views.TickerView)
# router.register(r'quote', views.QuoteView)


app_name = 'api'
urlpatterns = [
	path('', include(router.urls)),
]


