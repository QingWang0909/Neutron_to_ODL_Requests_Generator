# This python tool will clear the file content and make the file size be zero

import sys


def usage():
    print "Usage: python delete_file_content <file_name>"


def main():
    try:
        target = sys.argv[1]
    except:
        usage()
        exit(-1)

    with open(target, 'w'):
        pass


if __name__ == '__main__':
    main()


