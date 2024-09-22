from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from .models import Link
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from .models import Link

def scrape(request):
    if request.method == "POST":
        original_url = request.POST.get('site', '')

        # Ensure the URL starts with "http://" or "https://"
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url

        # Store the original URL in the session
        request.session['original_url'] = original_url
        
        try:
            page = requests.get(original_url)
            page.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Clear existing links if you want fresh data
            Link.objects.all().delete()

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                if link_address:
                    Link.objects.create(address=link_address, name=link_text)
            
            return redirect('/')

        except RequestException as e:
            error_message = f"An error occurred while trying to access the URL: {str(e)}"
            return render(request, 'scraper/result.html', {'error': error_message, 'original_url': original_url})

    # Retrieve data and original URL from the session
    data = Link.objects.all()
    original_url = request.session.get('original_url', '')
    
    return render(request, 'scraper/result.html', {'data': data, 'original_url': original_url})

def clear(request):
    Link.objects.all().delete()
    return render(request,'scraper/result.html')