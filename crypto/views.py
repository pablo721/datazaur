from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from utils.charts import Chart
from utils.order_currencies import *
from utils.etl import *
from website.models import Account, Config
from .forms import *
from .crypto_src import *
from markets.models import *
from data.models import *
from config import constants


class CryptoView(TemplateView):
	template_name = 'crypto/crypto.html'

	def get_context_data(self, **kwargs):
		currency = constants.DEFAULT_CURRENCY
		watchlists = []
		if self.request.user.is_authenticated:
			currency = self.request.user.user_account.currency_code
			watchlists = self.request.user.user_account.watchlists.all()

		currencies = Currency.objects.all()
		countries = Country.objects.all()
		tickers = CryptoFiatTicker.objects.all()

		return {'currency': currency, 'currencies': currencies, 'countries': countries, 'tickers': tickers,
				'watchlists': watchlists}


# table['Watchlist'] = table['Symbol'].apply(lambda
#                                                x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
# table['Portfolio'] = table['Symbol'].apply(lambda
#                                                x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")

def crypto(request):
	context = {}
	context['currencies'] = Currency.objects.all()

	coin_ids = []

	table = top_coins_by_mcap()
	table['Watchlist'] = table['Symbol'].apply(lambda
												   x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
	table['Portfolio'] = table['Symbol'].apply(lambda
												   x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")
	context['table'] = table.to_html(escape=False, justify='center')

	if request.user.is_authenticated:
		account = Account.objects.get(user=request.user)
		watchlist = Watchlist.objects.filter(user=account).first()
		coins = watchlist.coins.all()

		print(coins)
		context['watchlist_ids'] = [c.symbol.lower() for c in coins]
		print(context['watchlist_ids'])
		if account.currency:
			context['currency'] = account.currency.symbol
		else:
			context['currency'] = constants.DEFAULT_CURRENCY

	if request.method == 'GET':
		return render(request, 'crypto/crypto.html', context)

	elif request.method == 'POST':
		if not request.user.is_authenticated:
			return render(request, 'website/login_required.html', context)

		elif request.is_ajax and 'checked_symbols' in str(request.POST):
			print('ajax2')
			print(request.POST)
			symbols = request.POST['checked_symbols'].split(',')
			coin_ids = [symbol.split('_')[1].lower() for symbol in symbols if '_' in symbol]
			print(coin_ids)
			watchlist.coins.clear()
			for symbol in coin_ids:
				watchlist.coins.add(Cryptocurrency.objects.filter(symbol=symbol).first())
			context['watchlist_ids'] = coin_ids

		elif 'amount' in str(request.POST):
			print('add to portfolio')
			print(request.POST)
			coin_id = request.POST['coin']
			new_amount = request.POST['amount']
			portfolio = Portfolio.objects.get(user=account)
			if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id).exists():
				amount = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id)
				amount.amount += new_amount
				print(f'added {amount} to {coin_id}')
			else:
				amount = Amounts.objects.create(portfolio=portfolio, coin=coin_id, amount=new_amount)
				print(f'created {amount} of {coin_id}')
			amount.save()

		return HttpResponseRedirect(reverse('crypto:crypto', args=()))


def add_exchange(request):
	exchange_id = request.POST['exchange_id']
	value = request.POST['value']
	print(value)
	user = request.user.profile
	exchange = Exchange.objects.get(id=exchange_id)
	if value:
		user.exchanges.add(exchange)
		msg = 'added'
	else:
		user.exchanges.remove(exchange)
		msg = 'removed'
	return HttpResponse(msg)


class ExchangesView(ListView):
	template_name = 'crypto/exchanges.html'
	model = CryptoExchange

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['favourites'] = [exchange.id for exchange in self.request.user.account.exchanges.all()]
		print(context)
		return context


class DominanceView(DetailView):
	template_name = 'crypto/dominance.html'

	top_n_choices = [10, 20, 50, 100]
	mcap_col = f'Market cap (USD)'

	def get_queryset(self):
		return Cryptocurrency.objects.filter(price > 0)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
		top_n_choices.remove(top_n_coins)
		top_n_choices.insert(0, top_n_coins)
		PALETTE = [get_random_color() for i in range(top_n_coins)]
		df = pd.read_csv('crypto.csv', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
		df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
		df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
		# df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
		chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
		chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
		js_scripts = chart.get_js()
		context['charts'] = []
		context['charts'].append(chart.get_presentation())
		context['table'] = chart.get_html()
		context['js_scripts'] = js_scripts
		context['top_n_choices'] = top_n_choices
		return context


def dominance(request):
	context = {}
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
		if profile.currency:
			currency = profile.currency.symbol
	else:
		currency = DEFAULT_CURRENCY
	top_n_choices = [10, 20, 50, 100]
	mcap_col = f'Market cap (USD)'

	if request.method == 'GET':
		top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
		top_n_choices.remove(top_n_coins)
		top_n_choices.insert(0, top_n_coins)
		PALETTE = [get_random_color() for i in range(top_n_coins)]
		df = pd.read_csv('crypto.csv', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
		df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
		df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
		# df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
		chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
		chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
		js_scripts = chart.get_js()
		context['charts'] = []
		context['charts'].append(chart.get_presentation())
		context['table'] = chart.get_html()
		context['js_scripts'] = js_scripts
		context['top_n_choices'] = top_n_choices

		return render(request, 'crypto/dominance.html', context)


class GlobalMetricsView(TemplateView):
	template_name = 'crypto/global_metrics.html'

	def get_context_data(self, **kwargs):
		return {}


class CryptoCalendarView(TemplateView):
	template_name = 'crypto/calendar.html'


class NFTView(TemplateView):
	template_name = 'crypto/nft.html'


class DeFiView(TemplateView):
	template_name = 'crypto/defi.html'


class MoversView(TemplateView):
	template_name = 'crypto/movers.html'

	def get_context_data(self, **kwargs):
		filename = Config.objects.get(key='crypto_file') if Config.objects.get(
			key='crypto_file').exists() else 'crypto.csv'
		refresh_rate = Config.objects.get(key='refresh_rate') if Config.objects.get(
			key='refresh_rate').exists() else 600
		if filename in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(filename) < refresh_rate:
			coins = pd.read_csv(filename, index_col=0).iloc[:, :8]
		else:
			coins = top_coins_by_mcap().iloc[:, :8]
		coins.loc[:, 'Price'] = coins.loc[:, 'Price'].astype('float64').round(6)
		timeframe = request.GET['timeframe'] if 'timeframe' in str(request.GET) else '24h'
		timeframes = ['1h', '24h']
		timeframes.remove(timeframe)
		timeframes.insert(0, timeframe)
		sort_key = timeframe + ' Δ'
		gainers = coins.sort_values(by=sort_key, ascending=False)
		losers = coins.sort_values(by=sort_key, ascending=True)
		gainers = prepare_df_display(gainers)
		losers = prepare_df_display(losers)
		return {'timeframes': timeframes, 'gainers_table': gainers.to_html(justify='center', escape=False),
				'losers_table': losers.to_html(justify='center', escape=False)}


class WatchlistView(TemplateView):
	template_name = 'crypto/watchlist.html'
	model = PortfolioAmounts
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
						PortfolioAmounts.objects.create(watchlist=watchlist, coin=coin, amount=amount, source=exchange)
					else:
						amt = PortfolioAmounts.objects.filter(watchlist=watchlist).filter(coin=coin)
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
						if PortfolioAmounts.objects.filter(coin=coin).filter(watchlist=watchlist).exists():
							p = PortfolioAmounts.objects.filter(coin=coin).filter(watchlist=watchlist).first()
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
		context['watchlist'] = watchlist_prices(watchlist)

		print(f"Odreder currs: {context['currencies']}")

		context.update(self.forms)
		return context
