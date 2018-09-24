import dnac_helpers
from messaging_helper import *
import getopt, sys, env_lab

if __name__ == "__main__":

    #parse input options
    argv = sys.argv[1:]

    opts, args = getopt.getopt(argv, "d:", ["destination="])
    email_destination = ""
    for opt, arg in opts:
        if opt in ['-d', '--destination']:
            email_destination = arg

    if email_destination == "":
        print("An email destination is required")
        sys.exit(0)



    #go find all network devices in DNAC
    all_devices = dnac_helpers.list_network_devices()
    msg = ""

    #filter out only Switches and Hubs
    switches = [d for d in all_devices if d['family'] == 'Switches and Hubs']

    #build email message body with details ports of each switch
    for this_switch in switches:
        msg += "Details of " + this_switch['hostname'] + "\r\n"
        msg += dnac_helpers.get_port_status(this_switch['id'], ['trunk', 'routed'], ['down']) + "\r\n\n"


    smtp_server = create_smtp_server()
    email_message = create_message(email_destination, 'DNA Center Alert', message=msg)

    smtp_server.send_message(email_message)

