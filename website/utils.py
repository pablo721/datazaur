from data.constants import DEFAULT_CURRENCY
import pandas as pd
import pycountry
import country_currencies
from ipwhois import IPWhois
from .models import Account



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location(ip):
    return IPWhois(ip).lookup_whois()['asn_country_code']


def get_currency(country):
    return country_currencies.get_by_country(country)[0]


def setup_account(request, user):
    currency = 'USD'
    location = None
    ip = None
    try:
        ip = get_client_ip(request)
        location = get_location(ip)
        currency = get_currency(location)
        print(f'Found ip, location and currency')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        account = Account.objects.create(user=user, currency=currency, signup_ip=ip, signup_location=location)
        Watchlist.objects.create(creator=account, name='Watchlist', currency=currency)
        print(f'Account: {request.user.username} has been setup.')


