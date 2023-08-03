from flask import Flask, render_template, request
import requests
import os

# Fetch the API key from environment variables
api_key = os.getenv('WEATHER_API_KEY')
# Create an instance of the Flask class
app = Flask(__name__)

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather(location, key):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}")
        response.raise_for_status()  # If the request failed, this will raise a HTTPError
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None

# Route for the home page
@app.route('/')
def home():
    # Render the home page
    return render_template('home.html')

# Route for the weather page
@app.route('/weather', methods=['POST'])
def weather():
    # Get the location from the form data
    location = request.form.get('location')
    # Fetch the weather data
    weather_data = fetch_weather(location, api_key)
    if weather_data is None:
        return render_template('error.html', error="Could not fetch weather data. Please try again.")
    forecast = []
    # Prepare a list of forecast data
    for item in weather_data.get('list', []):
        forecast.append({
            'time': item['dt_txt'],
            'description': item['weather'][0]['description'],
            'icon': f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png"
        })
    # Render the weather page with the location and forecast data
    return render_template('weather.html', location=location, forecast=forecast)

# Start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)