import socket
import subprocess
import re

# Example list of server names
servers = ['example.com', 'localhost']  # Replace with your server names

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error as err:
        print(f"Could not resolve {hostname}: {err}")
        return None

def get_netmask(ip):
    try:
        # Run the `ip` command to get the interface configuration
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        
        # Find the netmask for the given IP address using a regex
        match = re.search(rf'{ip}/\d+', result.stdout)
        if match:
            return match.group()
        else:
            print(f"No netmask found for IP {ip}")
            return None
    except Exception as e:
        print(f"Error getting netmask: {e}")
        return None

def get_subnet(ip, netmask):
    import ipaddress
    try:
        network = ipaddress.IPv4Network(f"{netmask}", strict=False)
        return network
    except ValueError as e:
        print(f"Error calculating subnet: {e}")
        return None

for server in servers:
    ip_address = get_ip_from_hostname(server)
    if ip_address:
        print(f"IP Address of {server}: {ip_address}")
        netmask = get_netmask(ip_address)
        if netmask:
            print(f"Netmask for {ip_address}: {netmask}")
            subnet = get_subnet(ip_address, netmask)
            if subnet:
                print(f"Subnet: {subnet}")