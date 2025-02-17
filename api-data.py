import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")

cities = {
    "San Diego": (32.7167, -117.1367),
    "Cactus": (32.8795, -115.8910),  # approximate location in California
    "Julian": (33.0786, -116.6016),
    "Palm Springs": (33.8303, -116.5453),
    "Los Angeles": (34.0522, -118.2437),
    "Fresno": (36.7378, -119.7871),
    "San Francisco": (37.7749, -122.4194),
    "Sacramento": (38.5816, -121.4944),
    "Tahoe City": (39.1653, -120.1416),
    "Chico": (39.7285, -121.8375),
    "Mount Shasta": (41.4091, -122.1949),
    "Crescent City": (41.7558, -124.2026)
}

weather_data = []

for city, (lat, lon) in cities.items():
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()

        weather_info = {
            "city": city,
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "visibility": data.get('visibility', 'N/A'),
            "dew_point": round(data['main']['temp'] - ((100 - data['main']['humidity']) / 5), 2),
            "precipitation": data.get('rain', {}).get('1h', 0),
            "wind_speed": data['wind']['speed'],
            "wind_degree": data['wind']['deg'],
            "condition": data['weather'][0]['description'].capitalize(),
            "date_time": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        weather_data.append(weather_info)
    else:
        print(f"Error fetching data for {city}, status code {response.status_code}")

# Save data to a JSON file
with open("weather_data.json", "w") as file:
    json.dump(weather_data, file, indent=4)


