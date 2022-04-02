from django.contrib import admin
from .models import *


admin.site.register(Cryptocurrency)
admin.site.register(CryptoTicker)
admin.site.register(CryptoFiatTicker)
admin.site.register(CryptoExchange)
admin.site.register(CryptoWatchlist)
admin.site.register(PortfolioAmounts)
admin.site.register(PrivateKey)
admin.site.register(PublicKey)
# admin.site.register(NFT)
# admin.site.register(NFTCollection)

