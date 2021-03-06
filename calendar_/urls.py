from django.urls import path
from . import views


app_name = 'calendar_'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('economic/', views.EconCalendarView.as_view(), name='econ_calendar'),
    path('technology/', views.TechCalendarView.as_view(), name='tech_calendar'),
    path('crypto/', views.CryptoCalendarView.as_view(), name='crypto_calendar'),
    ]