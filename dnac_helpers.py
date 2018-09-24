
import sys
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


import env_lab      # noqa

DNAC = env_lab.DNA_CENTER['host']
DNAC_USER = env_lab.DNA_CENTER['username']
DNAC_PASSWORD = env_lab.DNA_CENTER['password']
DNAC_PORT = env_lab.DNA_CENTER['port']

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }


def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s:%s/api/v1/%s" % (controller_ip, DNAC_PORT, path)


def get_url(url):

    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


def list_network_devices():
    web_response = get_url("network-device")
    return web_response['response']


def get_device_id(ip_address):
    device = get_url("network-device/ip-address/%s" % ip_address)
    return device['response']['id']


def get_interfaces_by_ip(ipaddress):
    dev_id = get_device_id(ipaddress)
    interfaces = get_url("interface/network-device/%s" % dev_id)
    interface_response = interfaces['response']
    return interface_response


def get_trunk_port_status_by_ip(ipaddress):
    dev_id = get_device_id(ipaddress)
    interfaces = get_url("interface/network-device/%s" % dev_id)

    interface_response = interfaces['response']
    result = "Trunk port status\r\n\n"
    for int in interface_response:
        if(int['portMode'] == 'trunk'):
            result += 'Trunk port %s has current status of %s \r\n' % (int['portName'],int['status'])
        if (int['portMode'] == 'routed'):
            result += 'Routed port %s has current status of %s \r\n' % (int['portName'], int['status'])
    return result


def get_port_status(id, port_type, port_status):
    interfaces = get_url("interface/network-device/%s" % id)

    ports = interfaces['response']
    result = "Port status:\r\n"

    if port_type.__len__() > 0:
        ports = [d for d in ports if d['portMode'] in port_type]

    if port_status.__len__() > 0:
        ports = [d for d in ports if d['status'] in port_status]

    for interface in ports:
        result += 'Port %s(%s) has a status of %s\r\n' % \
                  (interface['portName'],interface['portMode'],interface['status'])

    return result