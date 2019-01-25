import dnac_helpers
from messaging_helper import *
import argparse
import servicenow_helpers

if __name__ == "__main__":

    # parse input options
    parser = argparse.ArgumentParser(description="Collect port details from DNA Center")
    parser.add_argument('-s', '--status', nargs='+', help='port status')
    parser.add_argument('-t', '--type', nargs='+', help='port type')
    parser.add_argument('-f', '--family', nargs='+', help="Family of device, Routers, Switches and Hubs")
    group = parser.add_argument_group('Output Destination')
    group.add_argument('--email_destination', nargs='+', help='Email report to provided destination')
    group.add_argument('--servicenow', action='store_true', help='Create an incident in ServiceNow')
    group.add_argument('--print', action='store_true', help='Print report to screen')

    args = parser.parse_args()

    if not (args.email_destination or args.servicenow or args.print):
        parser.error('At least 1 output destination is required.')

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

    # filter out by family arg
    if family:
        filtered_devices = [d for d in all_devices if d['family'] in family]
    else:
        filtered_devices = all_devices

    # build message body with details ports of each device
    found_port_count = 0

    for this_device in filtered_devices:
        msg += "Details of " + this_device['hostname'] + "\r\n"
        device_results = dnac_helpers.get_port_status(this_device['id'], port_type, port_status)
        msg += device_results['message'] + "\r\n\n"
        found_port_count += device_results['count']
    msg += 'Total port count: ' + str(found_port_count)

    # Look at the outputs and handle accordingly
    if args.email_destination:
        email_message = create_message(args.email_destination, 'DNA Center Alert', message=msg)
        smtp_server = create_smtp_server()
        smtp_server.send_message(email_message)

    if args.print:
        print(msg)

    if args.servicenow:
        if found_port_count > 0:
            new_incident = servicenow_helpers.create_incident(short_name='Cisco DNA port status report',
                                                              desc=msg,
                                                              impact=1,
                                                              urgency=1,
                                                              caller_email='ciscodnacenter@cisco.com',
                                                              assignment_group='Network')

            print('New Incident created: %s' % new_incident['number'])
        else:
            print('No matching ports found, ServiceNow incident not needed.')



