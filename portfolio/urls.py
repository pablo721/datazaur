from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'portfolio'
urlpatterns = [
    path('', views.PortfolioView.as_view(), name='portfolio'),
    ]


