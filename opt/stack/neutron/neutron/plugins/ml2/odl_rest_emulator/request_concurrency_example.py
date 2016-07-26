import threading
import sys
from time import sleep
import timeit

def rest_requeset():
    #print 'send request request'
    sleep(1)                        # Can change this to sleep(10) so we can clearly see
                                    # that all request request send simutanieously as the total run time only be 10 second
                                    # which means all request request runs at the same time


thread_pool = []
concurrecy_number = 65535

if __name__ == '__main__':

    t1 = timeit.default_timer()
    try:
        for i in range(concurrecy_number):
            t = threading.Thread(target=rest_requeset)
            t.daemon = True
            thread_pool.append(t)
            t.start()
    except KeyboardInterrupt:
        sys.exit(1)

    t.join()
    t2 = timeit.default_timer()

    print 'Total run time is: %s second' %(t2-t1)


