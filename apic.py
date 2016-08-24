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


def get_app_state(policy, app_id, app_name):
    for item in policy['response']:
        if {'appName': app_name, 'id': app_id} in item['resource']['applications']:
            return item['actionProperty']['relevanceLevel']
        else:
            continue


def update_app_state(event_status, policy, app_id, app_name):
    apic = os.environ.get('APIC_SERVER')

    if event_status == True:
        if get_app_state(policy, app_id, app_name) != "Business-Relevant":
            i = 0
            #loop through each of the 3 policy entries
            for item in policy['response']:
                a = 0
                #if we are looking at the business-relevant policy, add app
                if item['actionProperty']['relevanceLevel'] == "Business-Relevant":
                    policy['response'][i]['resource']['applications'].append({"id": app_id, "appName": app_name})
                    i += 1
                    continue
                #if we are looking at the business-irrelevant (or default) policy, remove app
                else:
                    #loop through each of the applications
                    for apps in item['resource']['applications']:
                        #if app matches, delete from business-irrelevant, else continue looping applications
                        if apps['id'] == app_id:
                            policy['response'][i]['resource']['applications'].pop(a)
                            break
                        else:
                            a += 1
                            continue
                i += 1
        return policy
    else:
        if get_app_state(policy, app_id, app_name) != "Business-Irrelevant":
            i = 0
            #loop through each of the 3 policy entries
            for item in policy['response']:
                a = 0
                #if we are looking at the business-irrelevant policy, add app
                if item['actionProperty']['relevanceLevel'] == "Business-Irrelevant":
                    policy['response'][i]['resource']['applications'].append({"id": app_id, "appName": app_name})
                    i += 1
                    continue
                #if we are looking at the business-relevant (or default) policy, remove app
                else:
                    #loop through each of the applications
                    for apps in item['resource']['applications']:
                        #if app matches, delete from business-relevant, else continue looping applications
                        if apps['id'] == app_id:
                            policy['response'][i]['resource']['applications'].pop(a)
                            break
                        else:
                            a += 1
                            continue
                i += 1
        return policy

def put_policy_update(service_ticket, policy, policy_scope):
    if policy != get_policy(service_ticket, policy_scope):
        apic = os.environ.get("APIC_SERVER")

        reqUrl = "https://{0}/api/v1/policy".format(apic)
        header = {"X-Auth-Token": service_ticket, "Content-type":"application/json"}

        r = requests.put(reqUrl, headers=header, json=policy['response'])

        if r.status_code == 202:
            task_id = r.json()['response']['taskId']
            if get_task(service_ticket, task_id)['response']['isError'] == False:
                return "taskId {0} completed without errors".format(task_id)
            else:
                return "taskId {0} failed with errors".format(task_id)
        else:
            r.raise_for_status()
    else:
        return "No changes made to policy"

def get_task(service_ticket, task_id):
    apic = os.environ.get("APIC_SERVER")

    reqUrl = "https://{0}/api/v1/task/{1}".format(apic, task_id)
    header = {"X-Auth-Token": service_ticket, "Content-type": "application/json"}

    r = requests.get(reqUrl, headers=header)

    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()

'''
#Code test block
policy_scope = "ed-qos"
app_name = "facebook"

#print get_app_state(get_policy(get_ticket(),policy_scope),get_app_id(get_ticket(),app_name),app_name)

old = open("old.json", "w")
new = open("new.json", "w")

old.write(json.dumps(get_policy(get_ticket(),policy_scope), indent=4))
new.write(json.dumps(update_app_state(False,get_policy(get_ticket(),policy_scope),get_app_id(get_ticket(),app_name),app_name), indent=4))

old.close()
new.close()

#print put_policy_update(get_ticket(),update_app_state(False,get_policy(get_ticket(),policy_scope),get_app_id(get_ticket(),app_name),app_name),policy_scope)
'''