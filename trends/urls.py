from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path


app_name = 'trends'
urlpatterns = [
    path('', login_required(TrendsView.as_view()), name='trends'),
    ]
