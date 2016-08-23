from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import pprint

api_url= 'http://localhost:8001/api/'

@csrf_exempt
def home(request):
    if request.POST:
        choice = str(request.POST['choice'])
        url = str(request.POST['url'])
        data = ""
        if choice == '1':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'scrape', params = get_data)

            if response.status_code == 200:
                response_data = response.json()
                abstract = response_data['Abstract']
                title = str(response_data['Title'])
                hpo_terms = response_data['HPO Terms']
                data+= "Title:\n" + title + "\n"
                data+="Abstract:\n" + abstract + "\n"
                data+="HPO Terms:\n"
                for term in hpo_terms:
                    data += str(term) + "\n"


        if choice == '2':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'annotate', params = get_data)
            if response.status_code == 200:
                response_data = response.json()
                data = {}
                data["annotated_terms"] = response_data['Annotated HPO Terms']
                data["annotated_abstract"] = response_data['Annotated Abstract']
                data= pprint.pformat(data, indent=4)
                

        if choice == '3':
            get_data={'url' : str(url)}
            response = requests.get(api_url+ 'phenopacket', params = get_data)
            if response.status_code == 200:
                response_data = response.json()
                phenopacket = response_data['phenopacket']
                data = phenopacket

        return HttpResponse(data)

    return render(request, 'main/index.html')

