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

def homepage(request):
	template = get_template('index.html')
	html = template.render(locals())
	return HttpResponse(html)

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
				attraction_img_url = str(location_soup.find("a", class_ = "js-photoswipe-item").get("href"))

				if Attractions.objects.filter(at_name = attraction_name).count() == 0:
					data = Attractions.objects.create(
								at_name = attraction_name,
								at_category = attraction_category,
								at_url = attration_url,
								at_description = attraction_content,
								at_img_url = attraction_img_url
							)
					data.save()
				print(attraction_name)
			except Exception as e:
				print(e)
	print(count)
	return redirect('/')

def load_attrations_data(request):
	attractions_data = Attractions.objects.all()
	data = serialize('json', attractions_data)
	return HttpResponse(data, content_type='json')

def search_attrations(request):
	template = get_template('search_result.html')
	keyword = request.GET.get('keyword', '')

	attractions_data = Attractions.objects.filter(Q(at_name__contains=keyword) | 
		Q(at_description__contains=keyword) | Q(at_category__contains=keyword))

	paginator = Paginator(attractions_data, 16) # Show 12 content per page
	page = request.GET.get('page')

	try:
		content = paginator.page(page)
	except PageNotAnInteger:
    # If page is not an integer, deliver first page.
		content = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		content = paginator.page(paginator.num_pages)

	# index = content.number
	max_index = len(paginator.page_range)

	try:
		addsport = request.POST['add_spot']
		count = 0 

		try:
			count = int(request.session['spot_num'])
			if count == 0:
				request.session['spot_num'] = 1
		except:
			request.session['spot_num'] = 1
		
		if count != 0:
			addreply = 1
			boo = True
			spots = []

			for i in range(count):
				spots.append(request.session['add_spot'+str(i)])

			for j in range(count):
				if spots[j] == addsport :
					boo = False
					addreply = 0
					break

			if boo == True :
				request.session['add_spot'+str(count)] = addsport
				request.session['spot_num'] = count + 1 
		else:
			request.session['add_spot'+str(count)] = addsport

	except:
		pass

	# if max_index > 8:
	# 	if index >= max_index - 6:
	# 		start_index = max_index - 7
	# 		end_index = max_index
	# 	else :	
	# 		start_index = index
	# 		end_index = index + 7
	# else:
	# 	start_index = 1
	# 	end_index = max_index
	
	# page_range = range(start_index, end_index)

	html = template.render(locals())
	return HttpResponse(html)

def itinerary(request):
	template = get_template('itinerary.html')

	count = 0
	attractions_data = []

	try:
		delspot = request.POST['del_spot']
		count = request.session['spot_num']
		spots = []
		delpoint = -1

		for i in range(count):
			spots.append(str(i))
			spots.append(request.session['add_spot'+str(i)])  

		print(spots)

		for i in range(count*2):
			if delspot == spots[i]:
				delpoint = spots[i-1]
		print(delpoint)

		del request.session['add_spot'+str(delpoint)]
		print('add_spot'+str(delpoint))

		for i in range(count):
			if i > int(delpoint):
				request.session['add_spot'+str(i-1)] = spots[(i+1)*2-1]
				print(request.session['add_spot'+str(i-1)])

		request.session['spot_num'] = count -1
		print('spot'+request.session['spot_num'])

	except:
		pass

	try:
		count = request.session['spot_num']
		spots = []

		for i in range(count):
			spots.append(request.session['add_spot'+str(i)]) 

		for i in range(count):
			attractions_data.append (Attractions.objects.get(at_name = spots[i]))

	except:
		alert = '尚無行程'

	html = template.render(locals())
	return HttpResponse(html)