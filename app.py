from flask import Flask
from flask import render_template
import apic
import weather

app = Flask(__name__)
event_status = False


@app.route('/')
def hello_world():
    # call the apic.py module to get some details on what is currently in play

    return render_template('index.html')

@app.route('/apic-test/')
def check_ticket():
    ticket = apic.get_ticket()
    answer_string = "ticket:" + ticket + " appId: " + apic.get_appid(ticket)
    return answer_string

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route('/status/')
def get_status():
    if (event_status == False):
        answer_string = "All is clear!"
    else:
        answer_string = "Currently in emergency state"
    return answer_string


@app.route('/event/on/')
def event_on():
    event_status = True
    policy_scope = "ed-qos"
    app_name = "facebook"
    service_ticket = apic.get_ticket()
    return apic.put_policy_update(service_ticket,apic.update_app_state(event_status,apic.get_policy(service_ticket,policy_scope),apic.get_app_id(service_ticket,app_name),app_name),policy_scope)


@app.route('/event/off/')
def event_off():
    event_status = False
    policy_scope = "ed-qos"
    app_name = "facebook"
    service_ticket = apic.get_ticket()
    return apic.put_policy_update(service_ticket,apic.update_app_state(event_status,apic.get_policy(service_ticket,policy_scope),apic.get_app_id(service_ticket,app_name),app_name),policy_scope)

@app.route('/event/toggle/')
def event_toggle():
    if (event_status == False):
        return redirect(url_for('/event/on/'))
    else:
        return redirect(url_for('/event/off/'))

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
