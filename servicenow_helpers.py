import requests
import json
import env_lab

snow_host = env_lab.SNOW['host']
snow_user = env_lab.SNOW['username']
snow_pass = env_lab.SNOW['password']


def get_user(email):
    # Set the request parameters
    url = 'https://%s/api/now/v1/table/sys_user?sysparm_limit=1&email=%s' % (snow_host, email)

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(snow_user, snow_pass), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        return ""

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result'][0]


def get_group(name):
    # Set the request parameters
    url = 'https://%s/api/now/table/sys_user_group?sysparm_limit=1&name=%s' % (snow_host, name)

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(snow_user, snow_pass), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        return ""

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result'][0]


def create_incident(short_name, desc, impact, urgency, caller_email, assignment_group):
    # Set the request parameters
    url = 'https://%s/api/now/v1/table/incident' % snow_host

    caller_id = get_user(caller_email)['sys_id']
    group_id = get_group(assignment_group)['sys_id']

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    request_date = {"short_description": short_name,
                    "description": desc,
                    "impact": impact,
                    "assignment_group": group_id,
                    "caller_id": caller_id,
                    "urgency": urgency}

    # Do the HTTP request
    response = requests.post(url, auth=(snow_user, snow_pass), headers=headers, data=json.dumps(request_date))

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result']
