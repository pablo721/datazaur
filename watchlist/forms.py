from django import forms
from .models import *
from data.models import Currency


class AddCoin(forms.Form):
    coin = forms.CharField(label='Coin', widget=forms.ChoiceField(choices=()))
    source = forms.CharField(label='Source', widget=forms.ChoiceField(choices=()))
    amount = forms.FloatField(label='Amount', initial=0, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['coin'].choices = [(c.symbol, f'{c.name} ({c.symbol})') for c in Cryptocurrency.objects.all()]
            self.fields['source'].choices = [(e.id, e.name) for e in CryptoExchange.objects.all()]
        except Exception as e:
            print(f'error: {e}')


class DeleteCoin(forms.Form):
    coin = forms.ChoiceField(label='Coin', choices=[])
    watchlist = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['coin'].choices = ((c.symbol, c.name) for c in kwargs['watchlist'].coins.all())
        except:
            pass


class ChangeCurrency(forms.Form):
    currency = forms.ChoiceField(label='Currency', choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['currency'].choices = ((c.id, c.name) for c in Currency.objects.all())
        except Exception as e:
            print(f'error: {e}')


class NewWatchlist(forms.Form):
    name = forms.CharField(label='Name', max_length=16)
    currency = forms.ChoiceField(label='Currency', choices=())
    source = forms.ChoiceField(label='Source', choices=())
    portfolio = forms.BooleanField(label='Portfolio', initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].choices = ((c.alpha_3, c.name) for c in Currency.objects.all())
        self.fields['source'].choices = ((e.id, e.name) for e in CryptoExchange.objects.all())


class DeleteWatchlist(forms.Form):
    watchlist = forms.ChoiceField(label='Watchlist', choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['watchlist'].choices = ((w.id, w.namee) for w in self.request.user.user_account.watchlists.all())
        except:
            pass


class SetSource(forms.Form):
    watchlist = forms.ChoiceField(label='Watchlist', choices=())
    coin = forms.ChoiceField(label='Coin', choices=(), initial=None)
    source = forms.ChoiceField(label='Source', choices=())
    set_for_all = forms.BooleanField(label='Set for all', initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['source'].choices = ((ex.id, ex.name) for ex in CryptoExchange.objects.all())
            self.fields['watchlist'].choices = ((w.id, w.name) for w in CryptoWatchlist.objects.filter(creator=kwargs['acc_id']))
            self.fields['coin'].choices = ((c.symbol, c.name) for c in CryptoWatchlist.objects.get(id=kwargs['watchlist_id']).coins.all())
        except Exception as e:
            print(f'Error: {e}')



