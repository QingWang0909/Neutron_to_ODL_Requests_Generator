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


if __name__ == '__main__':
    emulator = RestEmulator()

    start = timeit.default_timer()

    # Create Subnet Requests
    for i in range(concurrent_num):
        obj = Fake_Obj_Const.CreateSubnet
        obj['subnet'][0]['id'] = get_uuid()
        put_task_in_threads(emulator.create_subnet, obj)

    run_task_in_threads()

    end = timeit.default_timer()

    print 'Total run time is %s second' %(end - start)
    print 'All request already sent'










