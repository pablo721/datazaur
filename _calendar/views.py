from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *


class EconCalendarView(TemplateView):
	template_name = '_calendar/econ_calendar.html'


class TechCalendarView(TemplateView):
	template_name = '_calendar/tech_calendar.html'


class CryptoCalendarView(TemplateView):
	template_name = '_calendar/crypto_calendar.html'











