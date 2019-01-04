# Need to install requests package for python
# easy_install requests
import requests
import json

def get_user(email):
    # Set the request parameters
    url = 'https://dev71924.service-now.com/api/now/v1/table/sys_user?sysparm_limit=1&email=%s' % email

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'devnetSNOW1'

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        return ""

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result'][0]


def get_group(name):
    # Set the request parameters
    url = 'https://dev71924.service-now.com/api/now/table/sys_user_group?sysparm_limit=1&name=%s' % name

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'devnetSNOW1'

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        return ""

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result'][0]


def create_incident(short_name, desc, impact, urgency, caller_email, assignment_group):
    # Set the request parameters
    url = 'https://dev71924.service-now.com/api/now/v1/table/incident'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'devnetSNOW1'

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
    response = requests.post(url, auth=(user, pwd), headers=headers, data=json.dumps(request_date))

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['result']
