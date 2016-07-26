import threading

from time import ctime, sleep
import sys


threads_pool = []
concurrent_number = 200
def doMultiThreadConcurrency():                 # this is main thread

    try:
        t1 = threading.Thread(target=music)     # Thread-1, Do *NOT* put music() here
        threads_pool.append(t1)
        print t1.name

        t2 = threading.Thread(target=movie)     # Thread-2, Do *NOT* put movie() here
        threads_pool.append(t2)
        print t2.name

        for t in threads_pool:
            t.setDaemon(True)
            t.start()

        t.join()                                # Hang out Main thread until all child thread finished

    except KeyboardInterrupt:
        sys.exit(1)


def doSingleThread():
    music()
    movie()


def usage():
    print 'Usage : Enter 1 for single-thread ; Enter 2 for multi-thread'



def music():
    for i in range(2):
        print 'I am listening to music. %s' %ctime()
        sleep(1)



def movie():
    for i in range(2):
        print 'I am watching movies . %s' %ctime()
        sleep(5)


if __name__ == '__main__':

    var = int(raw_input("Enter 1 for single-thread ; Enter 2 for multi-thread: "))

    if var == 1:
        doSingleThread()
    elif var == 2:
        doMultiThreadConcurrency()
    else:
        usage()