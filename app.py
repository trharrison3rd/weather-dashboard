from flask import Flask, render_template
import requests
import os

api_key = os.getenv('WEATHER_API_KEY')

app = Flask(__name__)


def fetch_weather(location, api_key):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}")
    return response.json()

@app.route('/')
def home():
    return "Hello world!"

@app.route('/weather/<location>')
def weather(location):
    weather_data = fetch_weather(location,api_key)
    return render_template('home.html',location=location, weather=weather_data['weather'][0])

if __name__ == '__main__':
    app.run(debug=True)

