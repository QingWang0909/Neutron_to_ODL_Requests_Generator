
# This module is responsible for sending json to OpenDaylight Controller

from oslo_log import log as logging
from oslo_serialization import jsonutils
import requests
import pprint

LOG = logging.getLogger(__name__)


class ODLClient(object):

    def __init__(self, url, username, password, timeout):
        self.url = url
        self.timeout = timeout
        self.auth = (username, password)
        self.debug = False

    def set_debug_level(self, flag):
        if (flag == True):
            self.debug = True
        else:
            self.debug = False

    def sendjson(self, method, urlpath, obj):
        """Send json to Opendaylight Controller"""

        # Break Point Debugger
        # import pydevd
        # pydevd.settrace('192.168.56.1', port=8888, stdoutToServer=True, stderrToServer=True)

        headers = { 'Content-Type' : 'application/json' }
        data = jsonutils.dumps(obj, indent=2) if obj else None
        url = '/'.join([self.url, urlpath])
        LOG.debug("Sending METHOD (%(method)s) URL (%(url)s) JSON (%(obj)s)",
                  {'method': method, 'url': url, 'obj': obj})


        r = requests.request(method, url=url,
                             headers=headers, data=data,
                             auth=self.auth, timeout=self.timeout)

        # Print Response Content if send "get" rest request
        if(method == 'get' and self.debug == False):
            print r._content


        if(self.debug == True):
            pprint.pprint( vars(r) )


