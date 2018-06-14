#!/usr/bin/env/ python

import pprint
import shade

# Modify these values below (or read them in from the command line or environment)

# publickey_filename = '~/.ssh/id_rsa.pub'
publickey_filename = '/home/{}/.ssh/id_rsa.pub'.format(os.getusername())

cloud_name = 'indiana'
image_id = '57feb854-a3dd-4872-97a0-7a14513f5579'  # IU: Ubuntu 16.04 Devel and Docker v.1.14

flavor_name = 'm1.small'
server_name_pattern = 'demo_worker-{}'
number_servers = 2 

# Initialize. Set debug=True & http_debug=True if you want to see more detailed cloud activity
shade.simple_logging(debug=True, http_debug=True)
# shade.simple_logging(debug=False, http_debug=False)

# You should have a clouds.yaml file with one or more OpenStack clouds and their connection details.
# The Shade library will try to look for a clouds.yaml file in the following locations:
# - Current Directory
# - ~/.config/openstack
# - /etc/openstack

# An example clouds.yaml file:
# clouds:
#   somecloud:
#     identity_api_version: 3
#     auth:
#       username: jsmith
#       password: XXXXXXXXXXXXXXXXXXXXXXXXXXX
#       project_name: jsmith
#       auth_url: https://yourcloud.example.org:5000

# Initialize cloud
cloud = shade.openstack_cloud(cloud=cloud_name)
assert cloud

server_search_pattern = server_name_pattern.format('*')

for server in cloud.search_servers(server_search_pattern):
    pprint.pprint(server)

# Set the server username to the auth username. You can override this.
auth_username = cloud.auth['username']
server_username = auth_username

# Get image by name (Less reliable - prefer by ID below)
# image = cloud.get_image('Ubuntu 16.04 Non-GUI Base v.1.0')

# Get image by ID
image = cloud.get_image_by_id(image_id)
assert image

# Find a flavor by name
flavor = cloud.get_flavor(flavor_name)
assert flavor

# Get first internal IPv4 network that contains the cloud username
all_networks = cloud.get_internal_ipv4_networks()
network_name = '{}-net'.format(auth_username)  # On IU the network that works is `twetnam-network`
# network_name = '{}-api-net'.format(auth_username)  # On TACC the network that works is `tswetnam-api-net`
matching_networks = [net for net in all_networks if net.name == network_name]
assert matching_networks, 'No networks found matching: {}'.format(network_name)
network = matching_networks[0]
assert network

# Above should work. Otherwise print out the output of `cloud.get_internal_ipv4_networks()` and pick one
# On CyVerse and Jetstream  it's usually something like '<username>-net'
# pprint.pprint(all_networks)

keypairs = cloud.list_keypairs()

with open(publickey_filename, 'r') as public_key_file:
    public_key = public_key_file.read()
key_name = 'shade-key'
try:
    keypair = cloud.create_keypair(key_name, public_key)
except shade.exc.OpenStackCloudException as e:
    keypair = cloud.get_keypair(key_name)

# Set up things that should happen on boot (and maybe every reboot)
# See: https://cloudinit.readthedocs.io/en/latest/topics/examples.html

# Below is just an example. Customize as you need.

userdata_template = '''#cloud-config
users:
  - name: {username}
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
ssh_authorized_keys:
  - {public_key}
packages:
 - apt-transport-https
 - ca-certificates
 - curl
 - software-properties-common
runcmd:'''

# Install Singularity on Trusty (Ubuntu 14.04):
# userdata_template += '''
# - wget -O- http://neuro.debian.net/lists/trusty.us-ca.libre > /etc/apt/sources.list.d/neurodebian.sources.list
# - apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9'''

# For Singularity on Xenial (Ubuntu 16.04):
# userdata_template += '''
#  - wget -O- http://neuro.debian.net/lists/xenial.us-ca.libre > /etc/apt/sources.list.d/neurodebian.sources.list
#  - apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9'''

userdata_template += '''
 - apt-get update
'''

# userdata_template += '''
#  - apt-get install -y singularity-container
# '''

userdata_template += '''
final_message: "The system is finally up, after $UPTIME seconds"
'''

userdata = userdata_template.format(
    username=server_username,
    public_key=public_key
)

# Launch the servers
for i in range(number_servers):
    server_name = server_name_pattern.format(i)
    print('Launching {}...'.format(server_name))
    server = cloud.create_server(
        server_name,
        image=image,
        flavor=flavor,
        wait=True,
        auto_ip=True,
        network=network,
        key_name=key_name,
        userdata=userdata)
    pprint.pprint(server)

# You should now be able to SSH as the `root` user to the servers printed above
pass
