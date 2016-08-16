from flask import Flask
import apic
import weather
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, IMAPEX!'

@app.route('/ticket/')
def check_ticket():
    return apic.get_ticket()

@app.route('/weather/')
def check_weather():
    city = weather.getCity()
    state = weather.getState()
    temp = weather.getTemp(weather.getCurrentConditions())
    weather_description = weather.getWeather(weather.getCurrentConditions())
    weather_string = "The current weather in "+city+", "+state+" is "+str(temp)+" and "+weather_description
    return weather_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
