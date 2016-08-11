
def foo():
    print 'foo'

def bar():
    print 'bar'

def foobar():
    print 'foobar'

def quit():
    print 'Program Closed'
    exit(1)

if __name__ == '__main__':

    while True:
        dict = { '0' : foo,
                 '1' : bar,
                 '2' : foobar,
                 '9' : quit
                }

        try:
            choice = raw_input('Choose a number >>')
            dict[choice]()


        except(KeyError):
            print "Choice must be 0, 1 or 2"


