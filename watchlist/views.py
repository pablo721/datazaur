from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *
from .forms import *


class WatchlistView(TemplateView):
	template_name = 'watchlist/portfolio.html'
	model = CryptoWatchlist
	forms = {'new_watchlist': NewWatchlist, 'add_coin': AddCoin, 'set_source': SetSource, 'delete_coin': DeleteCoin,
			 'delete_watchlist': DeleteWatchlist, 'change_currency': ChangeCurrency}

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			return render(request, 'website/login_required.html')

		context = self.get_context_data(**kwargs)
		watchlist = context['watchlist']
		acc = request.user.user_account

		if 'add_coin' in str(request.POST):
			add_form = AddCoin(request.POST)
			if add_form.is_valid:
				form_data = add_form.cleaned_data

				if CryptoExchange.objects.filter(name=form_data['source']).exists():
					exchange = CryptoExchange.objects.get(name=form_data['source'])
				else:
					exchange = CryptoExchange.objects.get(name=constants.DEFAULT_CRYPTO_EXCHANGES[0])

				if Cryptocurrency.objects.filter(symbol=form_data['coin']).exists():
					coin = Cryptocurrency.objects.get(symbol=form_data['coin'])
					amount = float(form_data['amount'])
					if coin not in watchlist.coins.all():
						watchlist.coins.add(coin)
						watchlist.save()
						Amounts.objects.create(watchlist=watchlist, coin=coin, amount=amount, source=exchange)
					else:
						amt = Amounts.objects.filter(watchlist=watchlist).filter(coin=coin)
						amt.amount = form_data['amount']
						amt.source = exchange
						amt.save()
			else:
				print(f'Errors: {add_form.errors}')

		elif 'delete_coin' in str(request.POST):
			delete_form = DeleteCoin(request.POST)
			if delete_form.is_valid():
				form_data = delete_form.cleaned_data
				coin = Cryptocurrency.objects.get(symbol=form_data['coin'])
				watchlist.coins.delete(coin)
				watchlist.save()
			else:
				print(f'Errors: {delete_form.errors}')

		elif 'new_watchlist' in str(request.POST):
			watchlist_form = NewWatchlist(request.POST)
			if watchlist_form.is_valid():
				form_data = watchlist_form.cleaned_data
				form_data.update({'creator': request.user.user_account})
				CryptoWatchlist.objects.create(**form_data)
			else:
				print(f'Errors: {watchlist_form.errors}')


		elif 'delete_watchlist' in str(request.POST):
			if CryptoWatchlist.objects.filter(id=kwargs['watchlist_id']).filter(creator=acc).exists():
				CryptoWatchlist.objects.filter(id=kwargs['watchlist_id']).filter(
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

		return HttpResponseRedirect(reverse('crypto:watchlist', kwargs={'id': kwargs['id']}))

	# def get_queryset(self, **kwargs):
	# 	if self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
	# 			creator=self.request.user_user_account).exists():
	# 		return self.model.objects.filter(id=self.kwargs['watchlist_id']).filter(
	# 			creator=self.request.user_user_account).first().coins().all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		acc = self.request.user.user_account
		currency = acc.currency_code

		if 'watchlist_id' in kwargs.keys() and CryptoWatchlist.objects.filter(id=kwargs['watchlist_id']).filter(
				creator=acc).exists():
			watchlist = CryptoWatchlist.objects.get(id=kwargs['watchlist_id'])
		elif acc.users_watchlists.exists():
			watchlist = acc.users_watchlists.first()
		else:
			watchlist = None

		context['account'] = acc
		context['watchlists'] = acc.users_watchlists.all()
		context['currencies'] = ordered_currencies(currency)
		context['coins'] = Cryptocurrency.objects.all()
		context['watchlist'] = watchlist_prices(watchlist, constants.DEFAULT_CURRENCY)

		print(f"Odreder currs: {context['currencies']}")

		context.update(self.forms)
		return context



