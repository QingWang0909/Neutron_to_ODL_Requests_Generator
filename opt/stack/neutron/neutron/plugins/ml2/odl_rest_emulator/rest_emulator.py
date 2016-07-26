from networking_odl.common.client import  OpenDaylightRestClient
from time import sleep

class RestEmulator():

    def __init__(self):
        self.url = 'http://10.0.2.15:8080/controller/nb/v2/neutron'
        self.username = 'admin'
        self.password = 'admin'
        self.timeout = 10
        self.client = OpenDaylightRestClient(self.url, self.username, self.password, self.timeout)

    def create_subnet(self, fake_obj):
        method = 'post'
        urlpath = 'subnets'

        self.client.sendjson(method, urlpath, fake_obj)

    def list_networks(self, fake_obj):
        method = 'get'
        urlpath = 'networks'

        self.client.sendjson(method, urlpath, fake_obj)

    def create_network(self):
        pass


    # TODO: Confirm other urls
    def del_subnet(self, fake_obj):
        method = 'post'
        urlpath = 'subnets'

        client = OpenDaylightRestClient(self.url, self.username, self.password, self.timeout)
        client.sendjson(method, urlpath, fake_obj)




