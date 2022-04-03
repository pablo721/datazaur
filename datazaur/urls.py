
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('markets/', include('markets.urls'), name='markets'),
    path('data/', include('data.urls'), name='data'),
    path('news/', include('news.urls'), name='news'),
    path('trends/', include('trends.urls'), name='trends'),
    path('messenger/', include('messenger.urls'), name='messenger'),
    path('', include('website.urls'), name='website'),
]

