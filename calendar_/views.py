from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *


class CalendarView(TemplateView):
	template_name = 'calendar_/calendar.html'


class EconCalendarView(TemplateView):
	template_name = 'calendar_/econ_calendar.html'


class TechCalendarView(TemplateView):
	template_name = 'calendar_/tech_calendar.html'


class CryptoCalendarView(TemplateView):
	template_name = 'calendar_/crypto_calendar.html'











