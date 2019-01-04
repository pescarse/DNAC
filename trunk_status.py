import dnac_helpers
from messaging_helper import *
import argparse
import servicenow_helpers

if __name__ == "__main__":

    # parse input options
    parser = argparse.ArgumentParser(description="Collect port details from DNA Center")
    parser.add_argument('-e', '--email_destination', nargs='+', help='email to send report results')
    parser.add_argument('-s', '--status', nargs='+', help='port status')
    parser.add_argument('-t', '--type', nargs='+', help='port type')
    parser.add_argument('-f', '--family', nargs='+', help="Family of device")
    parser.add_argument('--servicenow', action='store_true', help='Create an incident in ServiceNow')
    parser.add_argument('--print', action='store_true', help='Print to screen, do not send email')

    args = parser.parse_args()

    port_status = args.status if args.status else []
    # Different ways to write if statements
    # if args.status: port_status = args.status
    # else: port_status = []

    port_type = args.type if args.type else []
    # Different ways to write if statements
    # if args.type:
    #    port_type = args.type
    # else:
    #    port_type = []

    family = args.family if args.family else []

    # go find all network devices in DNAC
    all_devices = dnac_helpers.list_network_devices()
    msg = ""

    # filter out only Switches and Hubs
    if family:
        switches = [d for d in all_devices if d['family'] in family]
    else:
        switches = all_devices

    # build email message body with details ports of each switch
    for this_switch in switches:
        msg += "Details of " + this_switch['hostname'] + "\r\n"
        msg += dnac_helpers.get_port_status(this_switch['id'], port_type, port_status) + "\r\n\n"

    if args.email_destination:
        email_message = create_message(args.email_destination, 'DNA Center Alert', message=msg)
        smtp_server = create_smtp_server()
        smtp_server.send_message(email_message)

    if args.print:
        print(msg)

    if args.servicenow:
        new_incident = servicenow_helpers.create_incident(short_name='Down Trunk Ports Detected',
                                                          desc=msg,
                                                          impact=1,
                                                          urgency=1,
                                                          caller_email='ciscodnacenter@cisco.com',
                                                          assignment_group='Network')

        print('New Incident created: %s' % new_incident['number'])




