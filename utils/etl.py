import pandas as pd

from crypto.models import *
from markets.models import *
from news.models import *
from economics.models import *


def watchlist_prices(watchlist, quote):
	result = pd.DataFrame(index={'symbol': []}, data={'name': [], 'amount': [], 'bid': [], 'ask': [], 'daily_delta': [],
													  'daily_vol': [], 'daily_low': [], 'daily_high': []})
	n = 0
	for coin in watchlist.coins.all():
		if CryptoFiatTicker.objects.filter(base=coin.symbol).filter(quote=quote).exists():
			n += 1
			result.loc[coin.symbol] = CryptoFiatTicker.objects.get(base=coin.symbol, quote=quote).__dict__
			if PortfolioAmounts.objects.filter(watchlist=watchlist).filter(coin=coin).exists():
				result.loc[coin.symbol, 'amount'] = PortfolioAmounts.objects.get(watchlist=watchlist, coin=coin).amount
			print(result.loc[coin.symbol])
	print(f'Found {n} out of {watchlist.count()} prices.')
	return result


