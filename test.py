import requests ,json 
#id = int(input("User id=>"))
url = f"http://localhost:8000/reply/unlike/"
headers = {"Content-type":"application/json","Authorization":"Token c14efedad6e015551251145804a35c9fb9981c5c"}
data = json.dumps({
  "id":4
})
r = requests.post(url,headers=headers,data=data).json()
print(r)