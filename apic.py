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

#print get_app_id(get_ticket(), "facebook")
