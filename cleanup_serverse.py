import shade

# Modify these values below (or read them in from the command line)

cloud_names = ['indiana', 'tacc', 'marana']
server_name_pattern = 'demo_worker-{}'

for cloud_name in cloud_names:
    print('Finding & deleting servers and keypairs in cloud: {}'.format(cloud_name))
    server_search_pattern = server_name_pattern.format('*')

    # Initialize. Set debug=True & http_debug=True if you want to see more detailed cloud activity
    shade.simple_logging(debug=False, http_debug=False)
    # shade.simple_logging(debug=True, http_debug=True)

    # Initialize cloud
    cloud = shade.openstack_cloud(cloud=cloud_name)

    # Find all servers matching a pattern
    for server in cloud.search_servers(server_search_pattern):
        # print(server.__dict__)
        print('Deleting {}...'.format(server.name))
        delete_result = cloud.delete_server(server, wait=True, delete_ips=True)
        print(delete_result)
    else:
        print('No servers found')

    # Delete keypair
    key_name = 'shade-key'
    keypair = cloud.get_keypair(key_name)
    if keypair:
        print('Deleting keypair {}...'.format(keypair.name))
        delete_result = cloud.delete_keypair(key_name)
        print(delete_result)
    else:
        print('No keypair found with name: {}'.format(key_name))
