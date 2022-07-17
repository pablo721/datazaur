import investpy
import pandas as pd
import pycountry
import country_currencies
import ccxt
from pycoingecko import CoinGeckoAPI
import yaml
import json
import re
from markets.models import Ticker, Quote
from news.models import Website
from website.models import Account, Log, Config, Update
from crypto.models import CryptoExchange, Cryptocurrency
from data.models import Asset, Country, Commodity, Currency
from config import constants
from crypto.crypto_src import get_coins_info
import datetime


def setup_all():
	funcs = [load_config, load_countries, load_currencies, map_currencies, load_fx_tickers, load_crypto_exchanges, load_cryptocomp_coins]
	tables = ['website_log', 'data_country', 'markets_currency', 'markets_currency', 'markets_ticker',
			  'crypto_cryptoexchange', 'crypto_cryptocurrency']
	timestamp = datetime.datetime.now()
	for func, table in zip(funcs, tables):
		try:
			print(f'setting: {table}')
			func()
			if not Update.objects.filter(table=table).exists():
				Update.objects.create(table=table, timestamp=timestamp)
			update = Update.objects.get(table=table)
			update.timestamp = timestamp
			update.save()
			Log.objects.create(source=table, timestamp=timestamp, status=0)

		except Exception as e:
			print(f'Error: {e}')
			Log.objects.create(source=table, timestamp=timestamp, status=1, message=f'Error: {e}')

	print(f'Finito setup.')


def load_websites(filepath='config/websites.yaml'):
	with open(filepath, 'r') as file:
		websites = yaml.safe_load(file)
		for k, v in websites.items():
			print(f'Site {k}')
			print(f'Selectors {v}')
			if not Website.objects.filter(url=k).exists():
				Website.objects.create(url=k)
			site = Website.objects.get(url=k)
			for selector in v:
				if not Selector.objects.filter(text=selector).exists():
					Selector.objects.create(text=selector)
				s = Selector.objects.get(text=selector)
				site.selectors.add(s)
				site.save()
				print(f'Loaded {len(v)} selectors for {k}')


def load_config(filepath='config/config.yaml'):
	ext = filepath.split('.')[-1].lower()
	with open(filepath, 'r') as cfg:
		if ext == 'json':
			cfg_data = json.load(cfg.read())
		elif ext in ['yaml', 'yml']:
			cfg_data = yaml.safe_load(cfg)
		else:
			return 'Wrong file type. \n ' \
				   'Need a json/yaml/yml config file.'

	n_upd = 0
	n = Config.objects.all().count()
	for k, v in cfg_data.items():
		if Config.objects.filter(key=k).exists():
			cfg = Config.objects.get(key=k)
			cfg.value = v
			cfg.save()
			n_upd += 1
		else:
			Config.objects.create(key=k, value=v)
	print(f'Added {Config.objects.all().count() - n} parameters to database. \n'
		  f'Updated {n_upd} parameters.')



def load_cryptocomp_coins():
	n = Cryptocurrency.objects.all().count()
	coins = get_coins_info().loc[:, ['Symbol', 'CoinName', 'Description', 'Algorithm', 'ProofType', 'AssetWebsiteUrl']]
	print(coins)
	print(coins.columns)
	coins.columns = ['symbol', 'name', 'description', 'hash_algorithm', 'proof_type', 'url']
	coins[['description', 'url']] = coins[['description', 'url']].apply(lambda x: x[:254])
	for i, row in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol=row['symbol']).exists():

			Cryptocurrency.objects.create(name=row['name'], symbol=row['symbol'], url=str(row['url'])[:254] if row['url'] else '',
											  description=str(row['description'])[:254] if row['description'] else '',
											  hash_algorithm=row['hash_algorithm'], proof_type=row['proof_type'])

	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies from Cryptocompare.')



def load_tickers(exchanges=constants.DEFAULT_CRYPTO_EXCHANGES):
	url = f'https://min-api.cryptocompare.com/data/v4/all/exchanges?api_key={API_KEY}'



def load_gecko_coins():
	n = Cryptocurrency.objects.all().count()
	gecko = CoinGeckoAPI()
	coins = pd.DataFrame(columns=['id', 'symbol', 'name'], data=gecko.get_coins_list()).set_index('symbol',
																								  inplace=True,
																								  drop=True)
	for i, r in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol__ilike=i).exists():
			Cryptocurrency.objects.create(symbol=i.lower(), name=r['name'].lower())
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptos from CoinGecko.')


def load_countries():
	countries = pycountry.countries
	n = Country.objects.all().count()
	for obj in countries:
		if not Country.objects.filter(name=obj.name).exists():
			Country.objects.create(code=obj.alpha_2, name=obj.name)
	print(f'Loaded {Country.objects.all().count() - n} countries to db. \n')


def load_currencies():
	currencies = pycountry.currencies
	n = Currency.objects.all().count()
	n_upd = 0
	for c in currencies:
		print(c)
		print(c.__dict__)
		try:
			if Currency.objects.filter(code=c.alpha_3).exists():
				currency = Currency.objects.get(code=c.alpha_3)
				currency.name = c.name[:63]
				n_upd += 1
			else:
				Currency.objects.create(name=c.name[:63], code=c.alpha_3)
		except Exception as e:
			print(f'Error {e}')
			continue
	print(f'Added {Currency.objects.all().count() - n}  currencies to db. \n'
		  f'Updated {n_upd}  currencies.')


def map_currencies():
	n = 0
	codes = {k: v[0] if v else None for k, v in country_currencies.CURRENCIES_BY_COUNTRY_CODE.items()}
	for country in Country.objects.all():
		code = codes[country.code]

		if Currency.objects.filter(code=code).exists():
			currency = Currency.objects.get(code=code)
			currency.issuer = country
			country.currencies.add(currency)
			country.save()
			n += 1
			print(f'Mapped {currency.name} ({currency.code}) to {country.name}')
	print(f'Mapped {n} currencies to countries.')


def load_crypto_exchanges():
	n = CryptoExchange.objects.all().count()
	default_exchanges = str(constants.DEFAULT_CRYPTO_EXCHANGES)
	for exchange_id in ccxt.exchanges:
		if re.search(exchange_id, default_exchanges):
			exchange_obj = getattr(ccxt, exchange_id)({'enableRateLimit': True})
			exchange_obj.load_markets()
			ex = CryptoExchange.objects.create(name=exchange_id, url=exchange_obj.urls['www'][:255])
			for country_code in exchange_obj.countries:
				if Country.objects.filter(code=country_code).exists():
					ex.countries.add(Country.objects.get(code=country_code))
			ex.save()
		else:
			CryptoExchange.objects.create(name=exchange_id)
	print(f'Loaded {CryptoExchange.objects.all().count() - n} exchanges to database.')



def connect_exchange(exchange_id, quote='USDT'):
	exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
	return pd.DataFrame(exchange.fetch_tickers()).transpose()


def filter_by_quote(ticker, quote='USDT'):
	return ticker.split('/')[1].__eq__(quote)



def load_fx_tickers(base='USD'):
	crosses = investpy.get_currency_crosses()
	for i, row in crosses.iterrows():
		if not Ticker.objects.filter(base=row['base']).filter(quote=row['second']).exists():
			Ticker.objects.create(base_asset_class='fx', base=row['base'], quote=row['second'], base_full_name=row['base_name'],
								  quote_full_name=row['second_name'])










