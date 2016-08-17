#! /usr/bin/python
'''
Python utility to perform API call to get current weather

'''

import requests, os, json

def getAPIKey():
    wundergroundKey = os.environ["WUNDERGROUND_KEY"]
    return wundergroundKey

def getCity():
    city = os.environ["WEATHER_CITY"]
    return city

def getState():
    state = os.environ["WEATHER_STATE"]
    return state

def getCurrentConditions():
    city = getCity()
    state = getState()
    wundergroundKey = getAPIKey()
    currentConditionsURL = "http://api.wunderground.com/api/"+wundergroundKey+"/conditions/q/"+state+"/"+city+".json"
    response = requests.get(currentConditionsURL)
    currentConditions = response.json()
    return currentConditions

def getTemp(currentConditions):
    currentTemp = currentConditions["current_observation"]["temp_f"]
    return currentTemp

def getWeather(currentConditions):
    currentWeather = currentConditions["current_observation"]["weather"]
    return currentWeather

#print json.dumps(getCurrentConditions(), indent=4)
#print getTemp(getCurrentConditions())
#print getWeather(getCurrentConditions())