#!/usr/bin/python
'''
	APIC-EM interface module for Event Driven QoS
	This module pulls needed APIC-EM APIs into python functions.

	The application is a simple demonstration of using APIC-EM
	dynamic QoS to modify QoS policies based on external factors
	such as weather events, power excursions, etc.
'''

__author__ = 'sluzynsk'

import requests
import os
import json

# To DOs:
# get service ticket, get application ID, install new policy,
# delete policy


def get_ticket():
    apic = os.environ.get('APIC_SERVER')
    username = os.environ.get('APIC_USERNAME')
    password = os.environ.get('APIC_PASSWORD')

    reqUrl = "https://{0}/api/v1/ticket".format(apic)
    payload = {'username': username, 'password': password}

    r = requests.post(reqUrl, json=payload)

    if (r.status_code == 200):
        return r.json()[u'response'][u'serviceTicket']
    else:
        r.raise_for_status()


def get_app_id(service_ticket, app_name):
    apic = os.environ.get('APIC_SERVER')

    reqUrl = "https://{0}/api/v1/application?name={1}".format(apic, app_name)
    header = {"X-Auth-Token": service_ticket}

    r = requests.get(reqUrl, headers=header)

    if (r.status_code == 200):
        return r.json()['response'][0]['id']
    else:
        r.raise_for_status()


def get_policy(service_ticket, policy_scope):
    apic = os.environ.get('APIC_SERVER')

    reqUrl = "https://{0}/api/v1/policy?policyScope={1}".format(apic, policy_scope)
    header = {"X-Auth-Token": service_ticket}

    r = requests.get(reqUrl, headers=header)

    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()


def get_app_state(service_ticket, policy_scope, app_name):
    policy = get_policy(service_ticket, policy_scope)
    app_id = get_app_id(service_ticket, app_name)

    for item in policy['response']:
        if {'appName': app_name, 'id': app_id} in item['resource']['applications']:
            return item['actionProperty']['relevanceLevel']
        else:
            continue


def update_app_state(event_status, service_ticket, policy_scope, app_name):
    apic = os.environ.get('APIC_SERVER')

    if event_status == True:
        if get_app_state(service_ticket, policy_scope, app_name) != "Business-Relevant":
            #enforce change here
            pass
        else:
            continue
    else:
        if get_app_state(service_ticket, policy_scope, app_name) != "Business-Irrelevant":
            #enforce change here
            pass
        else:
            continue


#print json.dumps(get_policy(get_ticket(), "ed-qos"), indent=4)
#print get_app_state(get_ticket(),"ed-qos","facebook")