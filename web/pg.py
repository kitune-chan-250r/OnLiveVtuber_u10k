import requests,json
url = 'http://localhost:8000/api/req/'
def post_api(data):
    return requests.post(url, data)


data = {'uid': 'testUUUUID', 'liver_name': 'test2liver',
        'gender': 'man', 'twitter_id': 'kitune', 'src': 'imgsrcurl'}
print(post_api(data))

print(requests.get(url).json())