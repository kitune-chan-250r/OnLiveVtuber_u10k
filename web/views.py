from django.shortcuts import render
import requests, json

# Create your views here.

def index(request):
    endpoint = 'http://localhost:8000/api/vtuber'
    search_word = request.GET.get('search_vtuber')
    if search_word is not None:
        endpoint += '/?search_query={0}'.format(search_word)
    print(endpoint)
    apidata = requests.get(endpoint).json()
    vtuber = []
    for v in apidata:
        vtuber.append({'uid': v['uid'], 'name': v['liver_name'], 'gender':v['gender']})
    

    data = { 'vtuber':vtuber
    }
    return render(request, 'index.html', data)