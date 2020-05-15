from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

#BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/?query={}"
#BASE_CRAIGSLIST_URL = "https://ahmedabad.craigslist.org/search/?query={}"
#BASE_CRAIGSLIST_URL = "https://www.google.com/search?safe=active&sxsrf=ALeKk02Zq9U1aBWyT98PLRmzlTIBqh1itQ%3A1589387675518&source=hp&ei=myG8XtSxHcyXlwT0v7_IBw&q={}&oq={}&gs_lcp=CgZwc3ktYWIQAzIFCAAQkQIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgjECc6CAgAEJECEIsDOggIABCDARCLAzoFCAAQiwM6BAgAEEM6BQgAEIMBOgcIABBDEIsDOgcIIxCxAhAnOgQIABAKULoPWPsvYJQ5aANwAHgBgAGQBYgB5iqSAQkyLTQuNC40LjKYAQCgAQGqAQdnd3Mtd2l6uAEC&sclient=psy-ab&ved=0ahUKEwiU67q-orHpAhXMy4UKHfTfD3kQ4dUDCAc&uact=5"
#BASE_CRAIGSLIST_URL = "https://poets.org/search?combine={}"
BASE_CRAIGSLIST_URL = "https://www.poetryfoundation.org/search?query={}"
BASE_SEARCH_URL = "https://www.poetryfoundation.org{}"

# Create your views here.

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    #response = requests.get("https://www.google.com/search?safe=active&sxsrf=ALeKk02Zq9U1aBWyT98PLRmzlTIBqh1itQ%3A1589387675518&source=hp&ei=myG8XtSxHcyXlwT0v7_IBw&q=hello+world&oq=hello+world&gs_lcp=CgZwc3ktYWIQAzIFCAAQkQIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgjECc6CAgAEJECEIsDOggIABCDARCLAzoFCAAQiwM6BAgAEEM6BQgAEIMBOgcIABBDEIsDOgcIIxCxAhAnOgQIABAKULoPWPsvYJQ5aANwAHgBgAGQBYgB5iqSAQkyLTQuNC40LjKYAQCgAQGqAQdnd3Mtd2l6uAEC&sclient=psy-ab&ved=0ahUKEwiU67q-orHpAhXMy4UKHfTfD3kQ4dUDCAc&uact=5")
    #response = requests.get("https://ahmedabad.craigslist.org/search/bbb?query=python%20tutor&sort=rel")
    #response = requests.get("https://losangeles.craigslist.org/search/bbb?query=python%20tutor&sort=rel")
    #response = requests.get("https://poets.org/search?combine=daffodils")
    #response = requests.get("https://www.poetryfoundation.org/search?query=Daffodils")
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    #print(soup.prettify())
    #print(soup.get_text())
    #post_titles = soup.find_all('a', {'class': 'result-title'})
    post_listings = soup.find_all('div', {'class': 'c-feature'})
    #post_listings = soup.find_all('li', {'class': 'result-row'})
    #post_titles = soup.find_all('a')
    #print(post_listings[0].text)
    print(post_listings[0].find(class_='c-txt').text)
    print(post_listings[0].find('a').get('href'))
    print(post_listings[0].find('a').text)
    print(post_listings[0].find(class_='c-txt_attribution').text)
    print(post_listings[0].find('p').text)
    #title1 = soup.title
    #print(title1)
    #print(data)
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
        final_postings.append((post_tag, post_title, post_url, post_writer, post_description))
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)