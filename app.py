from flask import Flask, render_template, request
import requests
import os

api_key = os.getenv('WEATHER_API_KEY')
api_key_new = "f99b90c163a7da224fd70f3194353e85"

app = Flask(__name__)


def fetch_weather(location, key):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key_new}")
    data = response.json()
    print(data)
    return data


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    weather_data = fetch_weather(location, api_key)
    forecast = []
    for item in weather_data['list']:
        forecast.append({
            'time': item['dt_txt'],
            'description': item['weather'][0]['description'],
            'icon': f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png"
        })
    return render_template('weather.html', location=location, forecast=forecast)



if __name__ == '__main__':
    app.run(debug=True)

