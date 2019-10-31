import requests,json
url = 'http://localhost:8000/api/onlive/'
def post_api(data):
    return requests.post(url, data)


data = {'uid_serializer': 'UCHBhnG2G-qN0JrrWmMO2FTA', 
		"live_title": "邪神きらら✞✟500人突破記念壺おじ耐久新人Vtuber",
        "live_url": "https://www.youtube.com/watch?v=Tj9fPLx75G0"}
print(post_api(data))

print(requests.get(url).json())

#print(requests.delete(url + 'UCHBhnG2G-qN0JrrWmMO2FTA'))