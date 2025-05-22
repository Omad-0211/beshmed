import requests
from utils.env import BASE_URL





def createUser(users):
    url = f"{BASE_URL}/users/"
    response = requests.post(url, json=users)
    
    try:
        data = response.json()
        return data
    except:
        return []
    
    
def getUser(user_id): 
    url = f"{BASE_URL}/users/{user_id}/"
    response = requests.get(url)
    
    try:
        data = response.json()
        return data['data']['results']
    except: 
        return []



def getTeacher():
    url = f"{BASE_URL}/teacher/"
    response = requests.get(url)
    
    try:
        print(response.status_code)
        data = response.json()
        return data['data']['results']
    except:
        return []


def getCategory():
    url = f"{BASE_URL}/category/"
    response = requests.get(url)
    
    try:
        print(response.status_code)
        data = response.json()
        return data['data']['results']
    except:
        return []


WORKERS = {
    "korrupsiya": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi",
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ],
    "darslar": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi",
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ],
    "nazorat": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi",
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ]
}