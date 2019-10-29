from django.shortcuts import render
import requests, json
from datetime import timedelta
from datetime import datetime
from dateutil.parser import parse
from pytz import timezone
import re, time

# Create your views here.
endpoint = 'http://localhost:8000/api/'

#str型 timeを受け取り'%Y-%m-%d %H:%M:%S'のdatetime.timedeltを返す
def time_jst(time):
    p = parse(time).astimezone(timezone('Asia/Tokyo'))
    return parse(p.strftime('%Y-%m-%d %H:%M:%S'))

#str型　startを受け取りdatetime.timedeltのpastを返す
def past_time(start):
    now = datetime.now()
    past = time_jst(str(now)) -  time_jst(start)
    return past

def deformed(start):
    secs = past_time(start).total_seconds()
    hours = int(secs / 3600)
    minutes = int(secs / 60) % 60

    if hours > 0:
        return '約{}時間'.format(hours)
    else:
        return '約{}分'.format(minutes)

def index(request):
    json_data = requests.get(endpoint + 'onlive/').json()
    data = {}
    livedata = []

    for i in json_data:
        past = deformed(i['start_time'])
        livedata.append({'liver_name': i['uid']['liver_name'],
                         'live_url': i['live_url'].replace('https://www.youtube.com/watch?v=', ''),
                         'live_title': i['live_title'],
                         'past_time': past,
                         'gender': i['uid']['gender']})

    data['livedata'] = livedata
    print(data)
    return render(request, 'index.html', data)


def index_old(request):
    search_word = request.GET.get('search_vtuber')
    endpoint += 'vtuber'
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

def vtuber(request):
    search_word = request.GET.get('search_vtuber')
    url = endpoint + 'vtuber'
    if search_word is not None:
        url += '/?search_query={0}'.format(search_word)
    print(url)
    apidata = requests.get(url).json()
    vtuber = []
    for v in apidata:
        vtuber.append({'uid': v['uid'], 'name': v['liver_name'], 'gender':v['gender']})
    

    data = { 'vtuber':vtuber
    }
    return render(request, 'vtuber_all.html', data)