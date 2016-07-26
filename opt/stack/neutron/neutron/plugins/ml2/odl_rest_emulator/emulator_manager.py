from rest_emulator import RestEmulator
from threading import Thread
from mock_object_template import MockObjects as Fake_Obj_Const

import sys
import timeit
import uuid

thread_pool = []
concurrent_num = 2

def get_uuid():
    return uuid.uuid1()
#
#
# def put_task_in_threads(target_func, obj):
#     try:
#         t = Thread(target=target_func, args=(obj,))
#         t.daemon = True
#         thread_pool.append(t)
#         t.start()
#
#     except KeyboardInterrupt:
#         sys.exit(1)
#
#
# def run_task_in_threads():
#     for i in thread_pool:
#         i.join()


if __name__ == '__main__':
    emulator = RestEmulator()

    start = timeit.default_timer()

    # Create Subnet Requests
    # for i in range(concurrent_num):
    #     obj = Fake_Obj_Const.CreateSubnet
    #     obj['subnet'][0]['id'] = get_uuid()
    #     put_task_in_threads(emulator.create_subnet, obj)
    #
    # run_task_in_threads()

    try:
        for i in range(concurrent_num):
            # Send List Network Requests
            # t1 = Thread( target=emulator.list_networks, args=(emulator.get_networks_request,) )
            # t1.daemon = True
            # thread_pool.append(t1)
            # t1.start()

            # Send Create Subnet Requests
            obj = Fake_Obj_Const.CreateSubnet
            obj['subnet'][0]['id'] = get_uuid()
            t2 = Thread( target=emulator.create_subnet, args=(obj,) )
            t2.daemon = True
            thread_pool.append(t2)
            t2.start()

    except KeyboardInterrupt:
        sys.exit(1)

    # t1.join()
    t2.join()

    # emulator.create_subnet_request(Fake_Obj_Const.CreateSubnet)

    end = timeit.default_timer()

    print 'Total run time is %s second' %(end - start)
    print 'All request already sent'










