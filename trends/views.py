from django.shortcuts import render
from django.views.generic.base import TemplateView


class TrendsView(TemplateView):
	template_name = 'trends/trends.html'

	def get_context_data(self, **kwargs):

		return 0

class TwitterView(TemplateView):
	template_name = 'trends/twitter.html'

	def get_context_data(self, **kwargs):
		scapped_news = {}
		news = scrap_news()
		for k, v in news.items():
			scapped_news[k] = pd.DataFrame(v).transpose().to_html(escape=False, justify='center')
		return {'scrapped_news': scapped_news}


class GoogleView(TemplateView):
	template_name = 'trends/google.html'

	def get_context_data(self, **kwargs):
		scapped_news = {}
		news = scrap_news()
		for k, v in news.items():
			scapped_news[k] = pd.DataFrame(v).transpose().to_html(escape=False, justify='center')
		return {'scrapped_news': scapped_news}


class RedditView(TemplateView):
	template_name = 'trends/reddit.html'

	def get_context_data(self, **kwargs):
		scapped_news = {}
		news = scrap_news()
		for k, v in news.items():
			scapped_news[k] = pd.DataFrame(v).transpose().to_html(escape=False, justify='center')
		return {'scrapped_news': scapped_news}


class TagsView(TemplateView):
	template_name = 'trends/tags.html'
	def get_context_data(self, **kwargs):
		scapped_news = {}
		news = scrap_news()
		for k, v in news.items():
			scapped_news[k] = pd.DataFrame(v).transpose().to_html(escape=False, justify='center')
		return {'scrapped_news': scapped_news}

