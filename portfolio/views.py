from django.shortcuts import render
from django.views.generic import TemplateView


class PortfolioView(TemplateView):
	template_name = 'portfolio/portfolio.html'


