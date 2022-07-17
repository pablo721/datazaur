from markets.models import Ticker



def cross_generate_tickers(base_list, quote_list):
	for base_asset in base_list:
		for quote_asset in quote_list:
			Ticker.objects.create(base=base_asset, quote=quote_asset)


