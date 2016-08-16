from flask import Flask
import apic
import weather

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, IMAPEX!'

@app.route('/ticket/')
def check_ticket():
    return apic.get_ticket()

@app.route('/weather/')
def check_weather():
    temp = weather.getTemp(weather.getCurrentConditions())
    weatherString = "The current temp is "+str(temp)
    return weatherString

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
