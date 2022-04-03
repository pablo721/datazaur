from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'data'
urlpatterns = [
    path('', views.DataView.as_view(), name='data'),
    path('macro/', views.MacroView.as_view(), name='macro'),
    path('fundamentals/', views.FundamentalsView.as_view(), name='fundamentals'),
    path('insider_trades/', views.InsiderTradesView.as_view(), name='insider_trades'),

    ]
