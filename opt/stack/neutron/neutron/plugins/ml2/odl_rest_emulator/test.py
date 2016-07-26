

from networking_odl.common import constants as odl_const

from neutron.plugins.ml2 import driver_api as api
from networking_odl.ml2 import mech_driver
from neutron.extensions import portbindings
from neutron.plugins.ml2 import plugin
from neutron import context

from oslo_config import cfg

from networking_odl.common.client import OpenDaylightRestClient

odl_opts = [
    cfg.StrOpt('url',
               help=_("HTTP URL of OpenDaylight REST interface.")),
    cfg.StrOpt('username',
               help=_("HTTP username for authentication")),
    cfg.StrOpt('password', secret=True,
               help=_("HTTP password for authentication")),
    cfg.IntOpt('timeout', default=10,
               help=_("HTTP timeout in seconds.")),
    cfg.IntOpt('session_timeout', default=30,
               help=_("Tomcat session timeout in minutes.")),
]


cfg.CONF.register_opts(odl_opts, "ml2_odl")

# FAKE_NETWORK = {'status': 'ACTIVE',
#                 'subnets': [],
#                 'name': 'net1',
#                 'provider:physical_network': None,
#                 'admin_state_up': True,
#                 'tenant_id': 'test-tenant',
#                 'provider:network_type': 'local',
#                 'router:external': False,
#                 'shared': False,
#                 'id': 'd897e21a-dfd6-4331-a5dd-7524fa421c3e',
#                 'provider:segmentation_id': None}

FAKE_SUBNET = {'ipv6_ra_mode': None,
               'allocation_pools': [{'start': '10.0.0.2',
                                     'end': '10.0.2.254'}],
               'host_routes': [],
               'ipv6_address_mode': None,
               'cidr': '10.0.2.0/24',
               'id': '72c56c48-e9b8-4dcf-b3a7-0813bb3bd839',
               'name': '',
               'enable_dhcp': True,
               'network_id': 'd897e21a-dfd6-4331-a5dd-7524fa421c3e',
               'tenant_id': 'test-tenant',
               'dns_nameservers': [],
               'gateway_ip': '10.0.2.1',
               'ip_version': 4,
               'shared': False}


FAKE_PLUGIN = plugin.Ml2Plugin
FALE_PLUGIN_CONTEXT =  context.Context

FAKE_SUBNET_CONTEXT = {'_original_subnet': None,
                       '_plugin': FAKE_PLUGIN,
                       '_plugin_context': FALE_PLUGIN_CONTEXT,
                       '_subnet': { 'allocation_pools': [{'end': '10.0.2.254', 'start': '10.0.2.2'}],
                                    'cidr': '10.0.2.0/24',
                                    'dns_nameservers': [],
                                    'enable_dhcp': True,
                                    'gateway_ip': u'10.0.2.1',
                                    'host_routes': [],
                                    'id': 'a4e8b7ba-4cd6-44a8-a55a-1962e50d4486',
                                    'ip_version': 4,
                                    'ipv6_address_mode': None,
                                    'ipv6_ra_mode': None,
                                    'name': u'subnet2',
                                    'network_id': u'4003b207-b2a7-4d12-9a17-6b0aedbbd03d',
                                    'shared': False,
                                    'subnetpool_id': None,
                                    'tenant_id': u'487827ffd19f4da99339ec1337bfc06f'}
                        }


# FAKE_SUBNET = { 'allocation_pools': [{'end': '10.0.2.254', 'start': '10.0.2.2'}],
#                                     'cidr': '10.0.2.0/24',
#                                     'dns_nameservers': [],
#                                     'enable_dhcp': True,
#                                     'gateway_ip': u'10.0.2.1',
#                                     'host_routes': [],
#                                     'id': 'a4e8b7ba-4cd6-44a8-a55a-1962e50d4486',
#                                     'ip_version': 4,
#                                     'ipv6_address_mode': None,
#                                     'ipv6_ra_mode': None,
#                                     'name': u'subnet2',
#                                     'network_id': u'4003b207-b2a7-4d12-9a17-6b0aedbbd03d',
#                                     'shared': False,
#                                     'subnetpool_id': None,
#                                     'tenant_id': u'487827ffd19f4da99339ec1337bfc06f'}
#
#


class SubnetContext():
    def __init__(self):
        self._original_subnet = None
        self._plugin = plugin.Ml2Plugin
        self._plugin_context = context.Context

        self._subnet = FAKE_SUBNET
        self.current = FAKE_SUBNET
        self.original = None

        # self._plugin_context.is_advsvc = False
        # self._plugin_context.is_admin = True


class RestEmulator(api.MechanismDriver):

    def __init__(self):
        self.odl_drv = mech_driver.OpenDaylightDriver()

    def getAttr(self):
        return

    def initialize(self):
        self.url = cfg.CONF.ml2_odl.url
        self.timeout = cfg.CONF.ml2_odl.timeout
        self.username = cfg.CONF.ml2_odl.username
        self.password = cfg.CONF.ml2_odl.password
        required_opts = ('url', 'username', 'password')
        for opt in required_opts:
            if not getattr(self, opt):
                raise cfg.RequiredOptError(opt, 'ml2_odl')
        self.vif_type = portbindings.VIF_TYPE_OVS
        self.vif_details = {portbindings.CAP_PORT_FILTER: True}
        self.odl_drv = mech_driver.OpenDaylightDriver()
        self.client = OpenDaylightRestClient(
                        self.url,
                        self.username,
                        self.password,
                        self.timeout
                      )

    def create_subnet(self, context):
        self.odl_drv.synchronize('create', odl_const.ODL_SUBNETS, context)



FAKE_OBJ = {'subnet': [{'ipv6_ra_mode': None, 'allocation_pools': [{'start': u'10.0.2.2', 'end': u'10.0.2.254'}], 'host_routes': [], 'ipv6_address_mode': None, 'cidr': u'10.0.2.0/24', 'id': u'7dc699ca-f705-4f40-ab22-1833d028e050', 'subnetpool_id': None, 'name': u'subnet3', 'enable_dhcp': True, 'network_id': u'f7db6cc2-ba08-47ba-8c3e-330546cd1161', 'tenant_id': u'487827ffd19f4da99339ec1337bfc06c', 'dns_nameservers': [], 'gateway_ip': u'10.0.2.1', 'ip_version': 4L, 'shared': False}]}


FAKE_OBJ1 = {
               'subnet':[
                  {
                     'ipv6_ra_mode':None,
                     'allocation_pools':[
                        {
                           'start':u'10.0.2.2',
                           'end':u'10.0.2.254'
                        }
                     ],
                     'host_routes':[

                     ],
                     'ipv6_address_mode':None,
                     'cidr':u'10.0.2.0/24',
                     'id':u'7dc699ca-f705-4f40-ab22-1833d028e058',
                     'subnetpool_id':None,
                     'name':u'subnet3',
                     'enable_dhcp':True,
                     'network_id':u'f7db6cc2-ba08-47ba-8c3e-330546cd1161',
                     'tenant_id':u'487827ffd19f4da99339ec1337bfc06c',
                     'dns_nameservers':[

                     ],
                     'gateway_ip':u'10.0.2.1',
                     'ip_version':4L,
                     'shared':False
                  }
               ]
            }


url = 'http://10.0.2.15:8080/controller/nb/v2/neutron'
username = 'admin'
password = 'admin'
timeout = 10
method = 'post'
urlpath = 'subnets'
obj = FAKE_OBJ1


client = OpenDaylightRestClient( url, username, password, timeout )

client.sendjson(method, urlpath, obj)

# emulator = RestEmulator()
# context = SubnetContext()

# import pprint
# pprint.pprint(vars(context))
#


# emulator.create_subnet(context)

# import pprint
# pprint.pprint(vars(context))
# with open("/home/ubuntu/text.txt", "wt") as fout:
#     pprint.pprint(vars(context), stream=fout)


