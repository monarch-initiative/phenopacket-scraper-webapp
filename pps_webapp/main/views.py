from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

api_url= 'http://localhost:8001/api/'

@csrf_exempt
def home(request):
    if request.POST:
        choice = str(request.POST['choice'])
        url = str(request.POST['url'])
        data = []
        if choice == '1':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'scrape', params = get_data)
            if response.status_code == 200:
                response_data = response.json()
                abstract = str(response_data['Abstract'])
                title = str(response_data['Title'])
                hpo_terms = str(response_data['HPO Terms'])
                data = data + [abstract, title, hpo_terms]

        if choice == '2':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'annotate', params = get_data)
            if response.status_code == 200:
                response_data = response.json()
                annotated_terms = str(response_data['Annotated HPO Terms'])
                annotated_abstract = str(response_data['Annotated Abstract'])
                data = data + [annotated_abstract, annotated_terms]

        if choice == '3':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'phenopacket', params = get_data)
            if response.status_code == 200:
                response_data = response.json()
                phenopacket = response_data['phenopacket']
                data = [phenopacket]

        response = '\n'.join(data)
        return HttpResponse(response)

    return render(request, 'main/index.html')

