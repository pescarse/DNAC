import dnac_helpers
from messaging_helper import *

if __name__ == "__main__":

    all_devices = dnac_helpers.list_network_devices()
    msg = ""

    switches = [d for d in all_devices if d['family'] == 'Switches and Hubs']

    for this_switch in switches:
        msg += "Details of " + this_switch['hostname'] + "\r\n"
        msg += dnac_helpers.get_trunk_port_status(this_switch['id']) + "\r\n\n"

    smtp_server = create_smtp_server()
    #msg = dnac_helpers.get_trunk_port_status("10.100.47.11")
    email_message = create_message('testuser@cisco.com', 'DNA Center Alert', message=msg)

    smtp_server.send_message(email_message)

