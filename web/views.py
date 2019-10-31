from django.shortcuts import render, redirect
import requests, json, re, time, bs4
from datetime import timedelta
from datetime import datetime
from dateutil.parser import parse
from pytz import timezone

# Create your views here.
#endpoint = 'http://localhost:8000/api/'
endpoint = 'https://onlive-vtuber-u10k.herokuapp.com/api/'

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

#uidからアイコンと表示名を取得
def img_src(cid):
    youtube = "https://www.youtube.com/channel/" + cid

    hed = {'Accept-Language': 'ja'}
    html_data = requests.get(youtube, headers=hed)

    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")

    try:
        name = parsed.find('h2', class_='epic-nav-item-heading').text
        icon_src = parsed.find('img', class_="channel-header-profile-image").get('src')
    except AttributeError:
        return False, False
    else:
        return name.strip(), icon_src.replace('s100', 's288')

#uidの登録があるか確認
def conf_cid(cid):
    url = endpoint + 'vtuber'
    apidata = requests.get(url).json()
    uids = [x['uid'] for x in apidata if x['uid'] == cid]
    if len(uids) < 1:
        return True
    else:
        return False
    


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

def vtuber(request):
    data = {}
    search_word = request.GET.get('search_vtuber')
    url = endpoint + 'vtuber'
    if search_word is not None:
        url += '/?search_query={0}'.format(search_word)
        data['search_word'] = search_word
    else:
        data['display'] = 'display:none'

    print(url)
    apidata = requests.get(url).json()
    vtuber = []
    for v in apidata:
        vtuber.append({'uid': v['uid'], 'name': v['liver_name'],
                     'gender':v['gender'], 'src': v['src']})
    
    data['vtuber'] = vtuber

    return render(request, 'vtuber_all.html', data)

"""def conf_cid(id):
    
    return 
"""

def request_page(request):
    data = {}
    conf = request.GET.get('conf_vtuber')
    if conf is not None and conf != "":
        res = conf_cid(conf)
        data['conf_res'] = res
        if res != False:
            name, src = img_src(conf)
            if name != False:
                data['src'] = src
                data['name'] = name
                data['uid'] = conf
            else:
               data['conf_res'] = False 
        data['status'] = True


    name = request.GET.get('name')
    uid = request.GET.get('uid')
    src = request.GET.get('src')
    gender = request.GET.get('gen')
    twitter = request.GET.get('twitter_id')

    print(name, uid, src, gender, twitter)

    if uid is not None and src != "":
        req_url = 'https://onlive-vtuber-u10k.herokuapp.com/api/req/'
        q = {'uid': uid, 'liver_name': name,
        'gender': gender, 'twitter_id': twitter, 'src': src}
        status = requests.post(req_url, q)
        if status.status_code == 201:
            return render(request, 'req_success.html')

    return render(request, 'request.html', data)

def request_manager(request):
    oauth = request.GET.get('pass')
    if oauth is not None and oauth == "aquamanji":
        url = 'https://onlive-vtuber-u10k.herokuapp.com/api/req/'
        apidata = requests.get(url).json()

        request_obj = []

        for i in apidata:
            request_obj.append({'uid': i['uid'],
                             'name': i['liver_name'],
                             'twitter': i['twitter_id'],
                             'gender': i['gender'],
                             'src': i['src']})
        data = {'request_obj': request_obj,
                'len': len(apidata)}
        return render(request, 'request_manager.html', data)
    else:
        return render(request, '404.html')

def accept_req(request):
    twitter = request.GET.get('twitter_id')
    uid = request.GET.get('uid')

    vtuber = {'uid':uid,
            'liver_name':request.GET.get('name'),
            'gender':request.GET.get('gen'),
            'src':request.GET.get('src')
    }

    requests.post(endpoint + 'vtuber/', vtuber)
    requests.delete(endpoint + 'req/' + uid + '/')
    
    return redirect('https://onlive-vtuber-u10k.herokuapp.com/reqmanag?pass=aquamanji')


def deny_req(request):
    uid = request.GET.get('uid')
    requests.delete(endpoint + 'req/' + uid + '/')
    return redirect('https://onlive-vtuber-u10k.herokuapp.com/reqmanag?pass=aquamanji')

def about_this_page(request):
    return render(request, 'about_this_page.html')
