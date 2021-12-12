import requests ,json 

url = "http://localhost:8000/comment/unlike/"
data = json.dumps({
  "id":2,
  "uid":2
})
headers = {"Content-type":"application/json"}
r = requests.post(url,data=data,headers=headers)
print(r.json())