from flask import Flask
import apic
import weather
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "This is the event driven Qos Application. Please see http://github.com/imapex/ed-qos for more information"

@app.route('/apic-test/')
def check_ticket():
    ticket = apic.get_ticket()
    answer_string = "ticket:" + ticket + " appId: " + apic.get_appid(ticket)
    return answer_string

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
