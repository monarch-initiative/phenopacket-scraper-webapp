from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import login, logout
from django.contrib import auth
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import requests

api_url= 'http://localhost:8001/api/'

def home(request):
    if request.POST:
        choice = str(request.POST['choice'])
        url = str(request.POST['url'])
        data = []
        if choice == '1':
            data={'content' : str(url)}
            response = requests.get(api_url+ 'scrape', params = data)
            if response.status_code == 200:
                response_data = response.json()
                abstract = response_data['Abstract']
                title = response_data['Title']
                hpo_terms = response_data['HPO Terms']
                data = data + [abstract, title, hpo_terms]

        if choice == '2':
            data={'content' : str(url)}
            response = requests.get(api_url+ 'annotate', params = data)
            if response.status_code == 200:
                response_data = response.json()
                annotated_terms = response_data['Annotated HPO Terms']
                annotated_abstract = response_data['Annotated Abstract']
                data = data + [annotated_abstract, annotated_terms]

        if choice == '3':
            data={'content' : str(url)}
            response = requests.get(api_url+ 'phenopacket', params = data)
            if response.status_code == 200:
                response_data = response.json()
                phenopacket = response_data['phenopacket']
                data = [phenopacket]

        context = {
        'data' : data,
        }

        return render(request, 'home.html', context)

    return render(request, 'home.html')

