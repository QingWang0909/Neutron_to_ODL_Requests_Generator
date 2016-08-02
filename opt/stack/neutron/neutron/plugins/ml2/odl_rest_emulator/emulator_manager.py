from rest_emulator import RestEmulator
from threading import Thread
from mock_object_template import MockObjects as Fake_Obj_Const

import sys
import timeit
import uuid


thread_pool = []
concurrent_num = 3


def get_uuid():
    return uuid.uuid1()


def put_task_in_threads(target_func, obj):
    try:
        t = Thread(target=target_func, args=(obj,))
        t.daemon = True
        thread_pool.append(t)
        t.start()

    except KeyboardInterrupt:
        sys.exit(1)


def run_task_in_threads():
    for i in thread_pool:
        i.join()


# Generate Subnet
def createSubnets(concurrent_num, network_uuid):
    for i in range(concurrent_num):
        obj = Fake_Obj_Const.Subnet
        obj['subnet'][0]['id'] = get_uuid()
        obj['subnet'][0]['network_id'] = network_uuid
        put_task_in_threads(emulator.create_subnet, obj)

    run_task_in_threads()


# Generate Network
def createNetworks(concurrent_num):
    for i in range(concurrent_num):
        obj = Fake_Obj_Const.Network
        obj['network'][0]['id'] = get_uuid()
        put_task_in_threads(emulator.create_network, obj)

    run_task_in_threads()


# Delete One Network
def delete_One_Network(uuid):
    emulator.del_network(uuid)


# Delete One Subnet
def delete_one_Subnet(uuid):
    emulator.del_subnet(uuid)


# Delete All Network
def delete_ALL_Network():
    pass


# Delete All Subnet
def delete_ALL_Subnet():
    pass


if __name__ == '__main__':
    emulator = RestEmulator()

    start = timeit.default_timer()

    # emulator.list_security_groups()

    # createSubnets(concurrent_num, '5f190e9e-5101-11e6-aa93-08002796ddd0')
    # createNetworks(concurrent_num)

    # delete_One_Network( 'dccc88f6-50fd-11e6-aa93-08002796ddd0' )
    # delete_one_Subnet( '43227e42-5146-11e6-aa93-08002796ddd0' )

    emulator.update_one_subnet('b262ac9a-514c-11e6-aa93-08002796ddd0', Fake_Obj_Const.Subnet)

    end = timeit.default_timer()

    print 'Total run time is %s second' %(end - start)
    print 'All request already sent'










