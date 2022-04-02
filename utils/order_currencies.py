from markets.models import Currency
import constants

default = constants.DEFAULT_CURRENCY


def ordered_currencies(code=default):
	first = code.upper()
	if not Currency.objects.filter(alpha_3=first).exists():
		return f'No currency matches {first}'
	first_curr = Currency.objects.filter(alpha_3=first)
	all_currs = Currency.objects.all().exclude(alpha_3=first)
	return first_curr.union(all_currs, all=True)


