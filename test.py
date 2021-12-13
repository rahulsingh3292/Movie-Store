import requests ,json 
#id = int(input("User id=>"))
url = f"http://localhost:8000/detail/my-subscription/11/"
headers = {"Content-type":"application/json","Authorization":"Token 37b963b87dbfee64e3dd565424bc18eb7777e099"}
r = requests.get(url,headers=headers)
if r.status_code == 200:
  print(r.json())
if r.status_code == 403:
  print("permission denied")
if r.status_code == 404:
  print("not found")