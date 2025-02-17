import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

cities = {
    "San Diego": (32.71442571123384, -117.1597479258551),
    "Cactus": (32.86499931741986, -114.88966323610104),  
    "Julian": (33.07855421177866, -116.60171282736363),
    "Palm Springs": (33.8303, -116.5453),
    "Los Angeles": (34.0522, -118.2437),
    "Fresno": (36.7378, -119.7871),
    "San Francisco": (37.7749, -122.4194),
    "Sacramento": (38.5816, -121.4944),
    "Tahoe City": (39.1671, -120.1428),
    "Chico": (39.7285, -121.8375),
    "Mount Shasta": (41.4092, -122.1949),
    "Crescent City": (41.7558, -124.2014),
}

#File path for JSON storage
FILE_PATH = "weather_data.json"

#Load existing data
try:
    with open(FILE_PATH, "r") as f:
        weather_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    weather_data = []

#Fetch data from API
for city, (lat, lon) in cities.items():
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        
        entry = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "visibility": data.get("visibility", "N/A"),
            "wind_speed": data["wind"]["speed"],
            "wind_degree": data["wind"]["deg"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        #Append new data
        weather_data.append(entry)


with open(FILE_PATH, "w") as f:
    json.dump(weather_data, f, indent=4)

