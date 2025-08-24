import sys
import os
import json
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
    data = client.droplets.list()
except Exception as e:
    print(f"Error: Unexpected error occurred while fetching droplets - {e}")
    sys.exit(1)

# Get JSON object of all droplets
droplet_list = data['droplets']

# Find droplet name supplied via cmd line
my_droplet = False
for droplet in droplet_list:
    if droplet['name'] == sys.argv[1]:
        # Save droplet object
        my_droplet = droplet
        break

# Make sure we found the droplet
if not my_droplet:
    print(f"Droplet {sys.argv[1]} not found!")
    exit(1)

# Save droplet id
droplet_id = my_droplet['id']

# Get firewall info
resp = client.droplets.list_firewalls(droplet_id=droplet_id)
print(json.dumps(resp, indent=4))