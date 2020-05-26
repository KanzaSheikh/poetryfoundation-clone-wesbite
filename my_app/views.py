from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_POETRYFOUNDATION_URL = "https://www.poetryfoundation.org/search?query={}"
BASE_SEARCH_URL = "https://www.poetryfoundation.org{}"
ABOUT_POETRYFOUNDATION_URL = "https://www.poetryfoundation.org/foundation/people"

# Create your views here.

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_POETRYFOUNDATION_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    post_listings = soup.find_all('div', {'class': 'c-feature'})
    
    final_postings = []
    for post in post_listings:
        if post.find(class_='c-txt'):
            post_tag = post.find(class_='c-txt').text
        else:
            post_tag = "N/A"
        if post.find('a'):
            post_title = post.find('a').text
        else:
            post_title = "N/A"
        if post.find('a'):
            post_url_id = post.find('a').get('href')  
            post_url = BASE_SEARCH_URL.format(post_url_id) 
        else:
            post_url = "#"
        if post.find(class_='c-txt_attribution'):
            post_writer = post.find(class_='c-txt_attribution').text
        else:
            post_writer = "N/A"
        if post.find('p'):
            post_description = post.find('p').text
        else:
            post_description = "N/A"
        if post.find('img'):
            post_image_url = post.find('img').get('srcset').split(',')[0]
            print(post_image_url)
        else:
            post_image_url = "static\images\K.jpg"  
        final_postings.append((post_tag, post_title, post_url, post_writer, post_description, post_image_url))

        
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
