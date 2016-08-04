
class MockObjects:

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
            'name':u'mynetwork3333',
            'admin_state_up':True,
            'tenant_id':u'487827ffd19f4da99339ec1337bfc06c',
            'provider:network_type':u'local',
            'vlan_transparent':None,
            'shared':False
         }
      ]
    }


    Port = {
    "ports": [
        {
            "admin_state_up": True,
            "allowed_address_pairs": [],
            "binding:host_id": "ubuntu-amd64",
            "binding:vif_details": [
                {
                    "port_filter": True
                }
            ],
            "binding:vif_type": "ovs",
            "binding:vnic_type": "normal",
            "device_id": "reserved_dhcp_port",
            "device_owner": "network:dhcp",
            "extra_dhcp_opts": [],
            "fixed_ips": [
                {
                    "ip_address": "10.0.2.2",
                    "subnet_id": "e1607dfd-f71e-45e5-a1d4-045f49d17fed"
                }
            ],
            "id": "e01b15fe-e1db-46aa-9c77-9bdc87b917fk",
            "mac_address": "FA:16:3E:E9:1C:36",
            "name": "",
            "network_id": "0459d012-9a2c-4814-b5e0-1852c8f98bf4",
            "security_groups": [],
            "tenant_id": "51cc435ba80242378ae46d8eab930190"
        }
    ]
    }