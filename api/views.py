from django.http import JsonResponse
import django_filters.rest_framework as rest_filters
from rest_framework import viewsets
from .serializers import *
from markets.models import Ticker
from crypto.models import Cryptocurrency
from data.models import Country, Currency, Commodity, Asset
from watchlist.models import Watchlist, Portfolio
from calendar_.models import CryptoEvent, EconEvent



class TickerView(viewsets.ModelViewSet):
	queryset = Ticker.objects.all()
	serializer_class = TickerSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]


class QuoteView(viewsets.ModelViewSet):
	queryset = Quote.objects.all()
	serializer_class = QuoteSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]




class CryptoView(viewsets.ModelViewSet):
	queryset = Cryptocurrency.objects.all()
	serializer_class = CryptoSerializer
	filter_backends = [rest_filters.DjangoFilterBackend]

	def get_queryset(self):
		return JsonResponse({'a': 1})


class WatchlistView(viewsets.ModelViewSet):
	queryset = Watchlist.objects.all()
	serializer_class = WatchlistSerializer


class PortfolioView(viewsets.ModelViewSet):
	queryset = Portfolio.objects.all()
	serializer_class = PortfolioSerializer


class CurrencyView(viewsets.ModelViewSet):
	queryset = Currency.objects.all()
	serializer_class = CurrencySerializer


class CountryView(viewsets.ModelViewSet):
	queryset = Country.objects.all()
	serializer_class = CountrySerializer


class CommodityView(viewsets.ModelViewSet):
	queryset = Commodity.objects.all()
	serializer_class = CommoditySerializer


class EconCalendarView(viewsets.ModelViewSet):
	queryset = EconEvent.objects.all()
	serializer_class = EconEventSerializer


class CryptoCalendarView(viewsets.ModelViewSet):
	queryset = CryptoEvent.objects.all()
	serializer_class = CryptoEventSerializer



