import json
import urllib.request

from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from .models import Attractions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.core.serializers import serialize # User for return json date with ajax
from django.db.models import Q
from django.template import RequestContext
def index(request):
	template = get_template('index.html')

	attractions_data = Attractions.objects.all()
	paginator = Paginator(attractions_data, 5) # Show 10 content per page
	page = request.GET.get('page')

	try:
		content = paginator.page(page)
	except PageNotAnInteger:
    # If page is not an integer, deliver first page.
		content = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		content = paginator.page(paginator.num_pages)

	index = content.number
	max_index = len(paginator.page_range)
	start_index = max_index - 7 if index >= max_index - 5 else index - 1 if index != 1 else 1
	end_index = max_index + 1 if index >= max_index - 6 else index + 7 if index != 1 else index + 8
	page_range = range(start_index, end_index)

	html = template.render(locals())
	return HttpResponse(html)

def scraping(request):	
	url = "http://travel.taichung.gov.tw/zh-tw/Attractions/ListByClassification" # 台中觀光旅遊網-景點列表 url
	with urllib.request.urlopen(url) as response:
		soup = BeautifulSoup(response, "html.parser")
	
	Attractions.objects.all().delete()
	count = 0
	for attractions_category in soup.find_all(class_ = "spot-category-section"):
		attraction_category = str(attractions_category.find("h4", class_ = "news-detail-title").text.split(" ")[0])
		for attraction in attractions_category.find_all(class_ = "item"):
			
			attraction_name = str(attraction.find("a").get("title"))

			base_url = "http://travel.taichung.gov.tw"
			attration_url = str(base_url + attraction.find("a").get("href"))

			try:
				with urllib.request.urlopen(attration_url) as response:
					location_soup = BeautifulSoup(response, "html.parser")

				attraction_content = str(location_soup.find("p", class_ = "highlight").text)

				if Attractions.objects.filter(at_name = attraction_name).count() == 0:
					data = Attractions.objects.create(
								at_name = attraction_name,
								at_category = attraction_category,
								at_url = attration_url,
								at_description = attraction_content
							)
					data.save()
				count+=1
				print(attraction_name)
			except Exception as e:
				print(e)
	print(count)
	return redirect('/')

def load_attrations_data(request):
	attractions_data = Attractions.objects.all()
	data = serialize('json', attractions_data)
	# print(data)
	return HttpResponse(data, content_type='json')

def search_attrations(request):
	template = get_template('index.html')
	keyword = request.GET.get('keyword', '')
	request.session['keyword'] = keyword
	keyword = request.session['keyword']
	print(keyword)
	attractions_data = Attractions.objects.filter(Q(at_name__contains=keyword) | 
		Q(at_description__contains=keyword) | Q(at_category__contains=keyword))

	paginator = Paginator(attractions_data, 5) # Show 10 content per page
	page = request.GET.get('page')

	try:
		content = paginator.page(page)
	except PageNotAnInteger:
    # If page is not an integer, deliver first page.
		content = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		content = paginator.page(paginator.num_pages)

	index = content.number
	max_index = len(paginator.page_range)

	if max_index > 8:
		if index >= max_index - 6:
			start_index = max_index - 7
			end_index = max_index
		else :	
			start_index = index
			end_index = index + 7
	else:
		start_index = 1
		end_index = max_index
	
	page_range = range(start_index, end_index)

	html = template.render(locals())
	return HttpResponse(html)

def homepage(request):
	template = get_template('junbotron.html')
	html = template.render(locals())
	return HttpResponse(html)

