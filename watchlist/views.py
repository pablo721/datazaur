from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import TemplateView
from config import constants
from crypto.models import *
from .models import *
from .forms import *
from .utils import watchlist_prices
from utils.fx import get_currency
from markets.models import Ticker



class PortfolioView(TemplateView):
	template_name = 'portfolio/portfolio.html'



class WatchlistView(TemplateView):
	template_name = 'watchlist/watchlist.html'
	model = Watchlist
	forms = {'new_watchlist': NewWatchlist, 'add_coin': AddCoin, 'set_source': SetSource, 'delete_coin': DeleteCoin,
			 'delete_watchlist': DeleteWatchlist, 'change_currency': ChangeCurrency}

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		print(request.POST)

		if not request.user.is_authenticated:
			return render(request, 'website/login_required.html')

		context = self.get_context_data(**kwargs)
		watchlist = context['watchlist']
		acc = request.user.user_account

		if 'watch_add_coin' in str(request.POST):
			coin_id = request.POST['watch_add_coin_select']
			currency_code = get_currency(request).code

			print(coin_id)
			if not Ticker.objects.filter(base=coin_id).filter(quote=currency_code).exists():
				ticker = Ticker.objects.create(base=coin_id, quote=currency_code, asset_class='crypto',
											   base_full_name=Cryptocurrency.objects.get(symbol=coin_id).name)
			else:
				ticker = Ticker.objects.get(base=coin_id, quote=currency_code)

			if ticker not in watchlist.tickers.all():
				watchlist.tickers.add(ticker)
				watchlist.save()




		elif 'delete_coin' in str(request.POST):
			delete_form = DeleteCoin(request.POST)
			if delete_form.is_valid():
				form_data = delete_form.cleaned_data
				coin = Cryptocurrency.objects.get(symbol=form_data['coin'])
				watchlist.coins.delete(coin)
				watchlist.save()
			else:
				print(f'Errors: {delete_form.errors}')

		elif 'new_watch' in str(request.POST):
			watchlist_form = NewWatchlist(request.POST)
			if watchlist_form.is_valid():
				form_data = watchlist_form.cleaned_data
				form_data.update({'creator': request.user.user_account})
				form_data.update({'currency': Currency.objects.get(code=form_data['currency'])})
				Watchlist.objects.create(**form_data)
			else:
				print(f'Errors: {watchlist_form.errors}')


		elif 'delete_watchlist' in str(request.POST):
			if Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(creator=acc).exists():
				Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(
					creator=context['account']).first().delete()

		elif 'set_source' in str(request.POST):
			source_form = SetSource(request.POST)
			if source_form.is_valid():
				form_data = source_form.cleaned_data
				if CryptoExchange.objects.filter(name=form_data['exchange']).exists():
					exchange = CryptoExchange.objects.get(name=form_data['exchange'])
					if form_data['set_for_all']:
						coins = watchlist.coins.all()
					else:
						coins = Cryptocurrency.objects.filter(symbol=form_data['coin'])
					for coin in coins:
						if Amounts.objects.filter(coin=coin).filter(watchlist=watchlist).exists():
							p = Amounts.objects.filter(coin=coin).filter(watchlist=watchlist).first()
							p.source = exchange
							p.save()
						else:
							print(f'Errors: {source_form.errors}')

		return HttpResponseRedirect(reverse('watchlist:watchlist'))

	# def get_queryset(self, **kwargs):
	# 	if self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
	# 			creator=self.request.user_user_account).exists():
	# 		return self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
	# 			creator=self.request.user_user_account).first().coins().all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		acc = self.request.user.user_account
		currency = get_currency(self.request)

		if 'watchlist_id' in kwargs.keys() and Watchlist.objects.filter(id=kwargs['watchlist_id']).filter(
				creator=acc).exists():
			watchlist = Watchlist.objects.get(id=kwargs['watchlist_id'])
		elif acc.users_watchlists.exists():
			watchlist = acc.users_watchlists.first()
		else:
			watchlist = Watchlist.objects.create(creator=acc, name='Watchlist')

		context['account'] = acc
		context['watchlists'] = acc.users_watchlists.all()
		context['currencies'] = constants.SORTED_CURRENCIES
		context['coins'] = Cryptocurrency.objects.all()
		context['watchlist'] = watchlist
		context['watchlist_prices'] = watchlist_prices(watchlist, currency)


		context.update(self.forms)
		return context



