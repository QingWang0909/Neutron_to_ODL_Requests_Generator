from rest_emulator import RestEmulator
from threading import Thread
from mock_object_template import MockObjects as Fake_Obj_Const

import sys
import timeit
import uuid

class EmulatorManager():
    def __init__(self):
        self.emulator = RestEmulator()

    def __get_uuid1(self):
        return uuid.uuid1()

    def __get_uuid4(self):
        return uuid.uuid4()


    def put_task_in_threads(self, target_func, obj):
        try:
            t = Thread(target=target_func, args=(obj,))
            t.daemon = True
            thread_pool.append(t)
            t.start()

        except KeyboardInterrupt:
            sys.exit(1)


    def run_task_in_threads(self):
        for i in thread_pool:
            i.join()


    # Generate Subnet
    def createSubnets(self, concurrent_subnet, network_uuid):
        for i in range(concurrent_subnet):
            obj = Fake_Obj_Const.Subnet
            obj['subnet'][0]['id'] = self.__get_uuid1()
            obj['subnet'][0]['network_id'] = network_uuid
            self.put_task_in_threads(self.emulator.create_subnet, obj)

        self.run_task_in_threads()


    # Generate Network
    def createNetworks(self, concurrent_client):
        for i in range(concurrent_client):
            obj = Fake_Obj_Const.Network
            obj['network'][0]['id'] = self.__get_uuid1()
            obj['network'][0]['tenant_id'] = self.__get_uuid4()
            self.put_task_in_threads(self.emulator.create_network, obj)

        self.run_task_in_threads()


    # Delete One Network
    def delete_One_Network(self, uuid):
        self.emulator.del_network(uuid)


    # Delete One Subnet
    def delete_one_Subnet(self, uuid):
        self.emulator.del_subnet(uuid)


    #
    # # Delete All Network
    # def delete_ALL_Network(self):
    #     pass
    #
    #
    # # Delete All Subnet
    # def delete_ALL_Subnet(self):
    #     pass
    #
    # # Delete All Port
    # def delete_ALL_Port(self):
    #     pass


concurrent_num = 2
thread_pool = []
if __name__ == '__main__':

    manager = EmulatorManager()

    while 1 :
        start = timeit.default_timer()

        cmd = raw_input('Enter Command: ')
        if cmd == 'q': print 'Emulator Program Closed' ; break

        if cmd == 'c':
            manager.createNetworks(concurrent_num)

        if cmd == 'cs':
            pass

        if cmd == 'd':
            manager.delete_One_Network('4ed65f44-5a5e-11e6-aa93-08002796ddd0')

        end = timeit.default_timer()

        # print 'Total run time is %s second' %(end - start)
        # print 'All request already sent'




# emulator.list_security_groups()

# emulator.create_port(Fake_Obj_Const.Port)

# createSubnets(concurrent_client, '5f190e9e-5101-11e6-aa93-08002796ddd0')


# delete_One_Network( 'dccc88f6-50fd-11e6-aa93-08002796ddd0' )
# delete_one_Subnet( '43227e42-5146-11e6-aa93-08002796ddd0' )

# emulator.update_one_subnet('b262ac9a-514c-11e6-aa93-08002796ddd0', Fake_Obj_Const.Subnet)


