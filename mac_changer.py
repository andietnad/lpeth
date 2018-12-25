#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    parser.parse_args()
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Specify an interface.")
    elif not options.new_mac:
        parser.error("Specify a new MAC.")
    return options

def change_mac(interface, new_mac):
    print("Changing interface " + interface + " MAC to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_searched_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_searched_result:
        return mac_searched_result.group(0)
    else:
        print("Could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("MAC was successfully changed.")
else:
    print("MAC did not get changed.")
