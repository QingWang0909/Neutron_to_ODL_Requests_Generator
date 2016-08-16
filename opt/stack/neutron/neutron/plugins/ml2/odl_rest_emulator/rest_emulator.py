# from networking_odl.common.client import  OpenDaylightRestClient
from time import sleep
from odl_client import ODLClient
# Wrapper class for Neutron Northbound APIs


class RestEmulator():

    def __init__(self):
        self.url = 'http://10.0.2.15:8080/controller/nb/v2/neutron'
        self.username = 'admin'
        self.password = 'admin'
        self.timeout = 10
        self.debug = False
        # self.client = OpenDaylightRestClient(self.url, self.username, self.password, self.timeout)
        self.client = ODLClient(self.url, self.username, self.password, self.timeout)

    def set_debug(self, flag):
        if(flag == True):
            self.client.set_debug_level(True)
        else:
            self.client.set_debug_level(False)

    # Neutron Network Northbound APIs
    def list_networks(self):
        method = 'get'
        urlpath = 'networks'
        self.client.sendjson(method, urlpath, None)

    def list_one_network(self, uuid):
        method = 'get'
        urlpath = 'networks/' + uuid
        self.client.sendjson(method, urlpath, None)

    def create_network(self, fake_obj):
        method = 'post'
        urlpath = 'networks'
        self.client.sendjson(method, urlpath, fake_obj)

    def del_network(self, uuid):
        method = 'delete'
        urlpath = 'networks/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron Subnet Northbound APIs
    def create_subnet(self, fake_obj):
        method = 'post'
        urlpath = 'subnets'
        self.client.sendjson(method, urlpath, fake_obj)

    def list_subnets(self):
        method = 'get'
        urlpath = 'subnets'
        self.client.sendjson(method, urlpath, None)

    def list_one_subnet(self, uuid):
        method = 'get'
        urlpath = 'subnets/' + uuid
        self.client.sendjson(method, urlpath, None)

    def update_one_subnet(self, uuid, new_fake_obj):     ###TODO: Attribute edit blocked by Neutron ?
        method = 'put'
        urlpath = 'subnets/' + uuid
        self.client.sendjson(method, urlpath, new_fake_obj)

    def del_subnet(self, uuid):
        method = 'delete'
        urlpath = 'subnets/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron Ports Northbound APIs
    def list_ports(self):
        method = 'get'
        urlpath = 'ports'
        self.client.sendjson(method, urlpath, None)

    def list_one_port(self, uuid):
        method = 'get'
        urlpath = 'ports/' + uuid
        self.client.sendjson(method, urlpath, None)

    def create_port(self, fake_obj):
        method = 'post'
        urlpath = 'ports'
        self.client.sendjson(method, urlpath, fake_obj)

    def del_port(self, uuid):
        method = 'delete'
        urlpath = 'ports/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron ScecurityGroup Northbound APIs
    def list_security_groups(self):
        method = 'get'
        urlpath = 'security-groups'
        self.client.sendjson(method, urlpath, None)

    def list_one_security_group(self, uuid):
        method = 'get'
        urlpath = 'security-groups/' + uuid
        self.client.sendjson(method, urlpath, None)

    def create_security_group(self, fake_obj):
        method = 'post'
        urlpath = 'security-groups'
        self.client.sendjson(method, urlpath, fake_obj)

    def del_security_group(self, uuid):
        method = 'delete'
        urlpath = 'security-groups/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron SecurityGroupRules Northbound APIs
    def list_security_grouprules(self):
        method = 'get'
        urlpath = 'security-group-rules'
        self.client.sendjson(method, urlpath, None)

    def list_one_security_grouprules(self, uuid):
        method = 'get'
        urlpath = 'security-group-rules/' + uuid
        self.client.sendjson(method, urlpath, None)

    def create_security_grouprules(self, fake_obj):
        method = 'post'
        urlpath = 'security-group-rules'
        self.client.sendjson(method, urlpath, fake_obj)

    def del_security_grouprules(self, uuid):
        method = 'delete'
        urlpath = 'security-group-rules/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron Floating IP Northbound APIs
    def list_floatingips(self):
        method = 'get'
        urlpath = 'floatingips'
        self.client.sendjson(method, urlpath, None)

    def list_one_floatingips(self, uuid):
        method = 'get'
        urlpath = 'floatingips/' + uuid
        self.client.sendjson(method, urlpath, None)

    def create_floatingips(self, fake_obj):
        method = 'post'
        urlpath = 'floatingips'
        self.client.sendjson(method, urlpath, fake_obj)

    def del_floatingips(self, uuid):
        method = 'delete'
        urlpath = 'floatingips/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron Router Northbound APIs
    def list_routes(self):
        method = 'get'
        urlpath = 'routers'
        self.client.sendjson(method, urlpath, None)

    def list_one_route(self, uuid):
        method = 'get'
        urlpath = 'routers/' + uuid
        self.client.sendjson(method, urlpath, None)



    # Neutron Firewall Northbound APIs
    def list_firewalls(self):
        method = 'get'
        urlpath = 'fw/firewalls'
        self.client.sendjson(method, urlpath, None)


    def list_one_firewall(self, uuid):
        method = 'get'
        urlpath = 'fw/firewalls/' + uuid
        self.client.sendjson(method, urlpath, None)

