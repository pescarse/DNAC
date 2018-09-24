import dnac_helpers
from messaging_helper import *
import getopt, sys
import argparse

if __name__ == "__main__":

    #parse input options
    parser = argparse.ArgumentParser(description="Collect port details from DNA Center")
    parser.add_argument('email_destination', help='email to send report results')
    parser.add_argument('-s', '--status', nargs='+', help='port status')
    parser.add_argument('-t', '--type', nargs='+', help='port type')
    parser.add_argument('--print', action='store_true', help='Print to screen, do not send email')

    args = parser.parse_args()
    email_destination = args.email_destination

    if args.status:
        port_status = args.status
    else:
        port_status = []

    if args.type:
        port_type = args.type
    else:
        port_type = []


    #go find all network devices in DNAC
    all_devices = dnac_helpers.list_network_devices()
    msg = ""

    #filter out only Switches and Hubs
    switches = [d for d in all_devices if d['family'] == 'Switches and Hubs']

    #build email message body with details ports of each switch
    for this_switch in switches:
        msg += "Details of " + this_switch['hostname'] + "\r\n"
        msg += dnac_helpers.get_port_status(this_switch['id'], port_type, port_status) + "\r\n\n"


    smtp_server = create_smtp_server()
    email_message = create_message(email_destination, 'DNA Center Alert', message=msg)

    if args.print:
        print(email_message)
    else:
        smtp_server.send_message(email_message)

