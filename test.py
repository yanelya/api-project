#this file is making requests to main.py (backend)
import requests

#location of api, where the server is running
BASE = "http://127.0.0.1:5000/"

#data we want to put into the db
data = [{"likes": 550, "name": "rest api", "views": 1000},
        {"likes": 40, "name": "how to code", "views": 200},
        {"likes": 3000, "name": "google mock interview", "views": 50000}]

for i in range(len(data)):
    respone = requests.put(BASE + "video/" + str(i), data[i])
    #.json() makes it not look like response object & actually be some sort of information
    print(respone.json()) 


input()
response = requests.get(BASE + "video/2")
print(response.json())