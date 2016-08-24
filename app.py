from flask import Flask
import apic
import weather

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "This is the event driven Qos Application. Please see http://github.com/imapex/ed-qos for more information"


@app.route('/apic-test/')
def check_ticket():
    ticket = apic.get_ticket()
    answer_string = "ticket:" + ticket + " appId: " + apic.get_appid(ticket)
    return answer_string


@app.route('/status/')
def get_status():
    # ticket = apic.get_ticket()
    if (1):
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
