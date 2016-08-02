
class MockObjects:

    # May not need this
    DelSubnet = {
        'subnet': [
            {
                'ipv6_ra_mode': None,
                'allocation_pools': [
                    {
                        'start': u'10.0.2.2',
                        'end': u'10.0.2.254'
                    }
                ],
                'host_routes': [

                ],
                'ipv6_address_mode': None,
                'cidr': u'10.0.2.0/24',
                'id': u'7dc699ca-f705-4f40-ab22-1833d028e078',
                'subnetpool_id': None,
                'name': u'subnet3',
                'enable_dhcp': True,
                'network_id': u'f7db6cc2-ba08-47ba-8c3e-330546cd1161',
                'tenant_id': u'487827ffd19f4da99339ec1337bfc06c',
                'dns_nameservers': [

                ],
                'gateway_ip': u'10.0.2.1',
                'ip_version': 4L,
                'shared': False
            }
        ]
    }


    Subnet = {
        'subnet': [
            {
                'ipv6_ra_mode': None,
                'allocation_pools': [
                    {
                        'start': u'10.0.2.2',
                        'end': u'10.0.2.254'
                    }
                ],
                'host_routes': [

                ],
                'ipv6_address_mode': None,
                'cidr': u'10.0.20.0/24',
                'id': u'7dc699ca-f705-4f40-ab22-1833d028e211',
                'subnetpool_id': None,
                'name': u'subnet3',
                'enable_dhcp': True,
                'network_id': u'5f190e9e-5101-11e6-aa93-08002796ddd0',
                'tenant_id': u'487827ffd19f4da99339ec1337bfc06c',
                'dns_nameservers': [

                ],
                'gateway_ip': u'10.0.2.1',
                'ip_version': 4L,
                'shared': False
            }
        ]
    }


    Network = {
      'network':[
         {
            'provider:physical_network': None,
            'mtu':0L,
            'id':u'46a18750-e165-4eef-8ef7-ebf2a7e3431f',
            'provider:segmentation_id':None,
            'router:external':False,
            'name':u'mynetwork22',
            'admin_state_up':True,
            'tenant_id':u'487827ffd19f4da99339ec1337bfc06c',
            'provider:network_type':u'local',
            'vlan_transparent':None,
            'shared':False
         }
      ]
    }




