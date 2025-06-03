import os
import sys

from pydo import Client

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} DropletName")
    sys.exit(1)
droplet_name = sys.argv[1]

# Get AuthToken
auth_token = os.getenv('DIGITALOCEAN_TOKEN')
if not auth_token:
    print("Error: DIGITALOCEAN_TOKEN environment variable not set.")
    print("Please set it (e.g., export DIGITALOCEAN_TOKEN='your_token_here')")
    sys.exit(1)

# Get a client object
client = Client(token=auth_token)

# Get JSON object of droplet data with error handling
try:
    droplet_list = client.droplets.list()
except Exception as e:
    print(f"Error: Unexpected error occurred while fetching droplets - {e}")
    sys.exit(1)

# Check if the API response has the expected structure
if 'droplets' not in droplet_list:
    print("Error: Unexpected API response format - missing 'droplets' key")
    sys.exit(1)

# Get JSON object of all droplets
droplets = droplet_list['droplets']

# Find droplet name supplied via cmd line
my_droplet = None
for droplet in droplets:
    if droplet['name'] == droplet_name:
        # Save droplet object
        my_droplet = droplet
        break

# Make sure we found the droplet
if my_droplet is None:
    print(f"Droplet {droplet_name} not found!")
    sys.exit(1)

# Access the 'networks' key within the my_droplet object.
if 'networks' not in my_droplet:
    print(f"Error: Droplet {droplet_name} has no network information")
    sys.exit(1)
networks = my_droplet['networks']

# Access the 'v4' key within 'networks'. This is a list of IPv4 network details.
if 'v4' not in networks:
    print(f"Droplet {droplet_name} has no IPv4 network information")
    sys.exit(1)
ipv4_networks = networks['v4']

# Iterate through the IPv4 networks to find the one with "type": "public".
public_ip_address = None
for network_info in ipv4_networks:
    if network_info['type'] == 'public':
        public_ip_address = network_info['ip_address']
        break

if public_ip_address is None:
    print(f"Unable to locate IP for {droplet_name}")
    sys.exit(1)

print(public_ip_address)
