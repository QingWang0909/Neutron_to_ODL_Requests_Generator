from rest_emulator import RestEmulator
from threading import Thread
from mock_object_template import MockObjects as Fake_Obj_Const
from connect_db import connect
from mysql.connector import MySQLConnection, Error

import sys
import timeit
import uuid
import binascii

class EmulatorManager():
    def __init__(self):
        self.emulator = RestEmulator()
        try:
            self.conn = connect()
            self.cursor = self.conn.cursor()
        except Error as e:
            print (e)

    def __get_uuid1(self):
        return uuid.uuid1()

    def __get_uuid3(self):
        return uuid.uuid3()

    def __get_uuid5(self):
        return uuid.uuid5()

    def __get_uuid4(self):
        return uuid.uuid4()

    # convert UUID to string for mysql storage
    def __uuid_hex_to_string(self, input_s):
        return uuid.UUID(input_s).urn[9:]


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



    # List All Networks
    def list_all_networks_db(self):
        try:
            mysql = """SELECT * FROM networks"""

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            print('Total Network Numbers: ', self.cursor.rowcount)
            for i, row in enumerate(rows):
                print "Network ", i + 1, " UUID: ", uuid.UUID(row[2])

        except Error as e:
            print (e)


    def __delete_all_networks_db(self):
        try:
            mysql = """SELECT * FROM networks"""

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            for row in rows:
                # Send request to ODL
                self.emulator.del_network( row[2] )

                mysql1 = """DELETE FROM networks WHERE network_id = %s"""
                args1 = (row[2], )

                self.cursor.execute(mysql1, args1)
                self.conn.commit()

        except Error as e:
            print (e)


    def __delete_all_subnets_db(self):
        try:
            mysql = """SELECT * FROM subnets"""

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            for row in rows:
                # Send request to ODL
                self.emulator.del_subnet( row[4] )

                mysql1 = """DELETE FROM subnets WHERE network_id = %s"""
                args1 = (row[3], )

                self.cursor.execute(mysql1, args1)
                self.conn.commit()

        except Error as e:
            print (e)


    # TODo: Change the emulator API to delete ports
    def __delete_all_ports_db(self):
        try:
            mysql = """SELECT * FROM ports"""

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            for row in rows:
                # Send request to ODL
                self.emulator.del_network( uuid.UUID(row[3]).urn[9:] ) # convert UUID to string for northbound urlpath concatenate

                mysql1 = """DELETE FROM ports WHERE network_id = %s"""
                args1 = (row[3], )

                self.cursor.execute(mysql1, args1)
                self.conn.commit()

        except Error as e:
            print (e)


    def __insert_networks_db(self, network_id, tenant_id, network_name):
        try:
            mysql = """INSERT INTO networks(tenant_id, network_id, network_name) VALUES(%s, %s, %s)"""

            args = (tenant_id, network_id, network_name)

            self.cursor.execute(mysql, args)

            self.conn.commit()

        except Error as e:
            print(e)


    def __insert_subnets_db(self, subnet_obj):
        try:
            mysql = """INSERT INTO subnets(tenant_id, subnet_name, network_id, subnet_id) VALUES (%s, %s, %s, %s)"""

            args = (subnet_obj['subnet'][0]['tenant_id'], subnet_obj['subnet'][0]['name'],
                    subnet_obj['subnet'][0]['network_id'], subnet_obj['subnet'][0]['id'])

            self.cursor.execute(mysql, args)

            self.conn.commit()

        except Error as e:
            print(e)

    # TODO: in CLI, list all subnets
    # TODO: check UUID, and check if exists in DB
    def check_network_uuid(self, input_s):

        # Test input_s UUID Validation & if UUID exists in Database
        try:
            uuid_obj = uuid.UUID(input_s)

            mysql = "select * from networks where network_id = %s"
            args = (input_s,)

            self.cursor.execute(mysql, args)
            self.conn.commit()

        except ValueError as e:
            print (e)
            return False

        except Error as e:
            print (e)
            return False

    # Delete All Resources
    def delete_all_resource(self):
        self.__delete_all_ports_db()
        self.__delete_all_subnets_db()
        self.__delete_all_networks_db()


    # Generate Subnet by one network UUID
    def createSubnets(self, concurrent_subnet, network_uuid_string):
        for i in range(concurrent_subnet):
            obj = Fake_Obj_Const.Subnet

            obj['subnet'][0]['network_id'] = network_uuid_string
            obj['subnet'][0]['id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)

            # fetch tenant_id based on network_id
            try:
                mysql = """select * from networks where network_id = %s"""

                args = (network_uuid_string, )

                self.cursor.execute(mysql, args)

                row = self.cursor.fetchone()
                obj['subnet'][0]['tenant_id'] = row[1]

            except Error as e:
                print (e)


            self.__insert_subnets_db(obj)
            self.put_task_in_threads(self.emulator.create_subnet, obj)

        self.run_task_in_threads()


    # Generate Network
    def createNetworks(self, concurrent_client):
        for i in range(concurrent_client):
            obj = Fake_Obj_Const.Network
            obj['network'][0]['id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)
            obj['network'][0]['tenant_id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)

            self.__insert_networks_db(obj['network'][0]['id'], obj['network'][0]['tenant_id'], obj['network'][0]['name'])
            self.put_task_in_threads(self.emulator.create_network, obj)

        self.run_task_in_threads()


    # Delete One Network
    def delete_One_Network(self, uuid):
        self.emulator.del_network(uuid)

    # Delete One Subnet
    def delete_one_Subnet(self, uuid):
        self.emulator.del_subnet(uuid)


concurrent_num = 200
thread_pool = []
manager = EmulatorManager()


def quit():
    print ("Program Closed! ")
    exit(1)


def del_all():
    while True:
        print ("\nThis operation will delete all the resoureces allocated, are you sure? (Y/N) ")
        print ("[0]: No")
        print ("[1]: Yes")

        try:
            choice = raw_input("Please select a number ( 0 ~ 1 ) >> ")
            if(choice == '0'):
                return

            elif(choice == '1'):
                print "delate resoureces!!"
                manager.delete_all_resource()
                return


        except(KeyError):
            print "Your input is not an integer, please enter an integer"


def list():
    manager.list_all_networks_db()


def check_int(input_s):
    try:
        int(input_s)

    except ValueError:
        print ("Your input is not an integer, please enter an interger")
        return False


    if (int(input_s) > 0 and int(input_s) <= 2500):
        return True
    else:
        print ("Your input is not in a valid range, please enter an valid interger")
        return False




def create_subnet():
    while True:
        print ("\n\nSUBNET Menu")
        print (">>How do you want to simulate create_subnet rest requests ?")
        print (">[0]: Quit Program")
        print (">[1]: List all existing network UUID")
        print (">[2]: Simulate multiple create_subnet rest requests under one network UUID")
        print (">[9]: Back to Upper Menu")


        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if (choice == '0'):
                quit()

            elif (choice == '1'):
                manager.list_all_networks_db()

            elif (choice == '2'):
                uuid_input = raw_input("Please enter the selected Network UUID number: ") # use database to reteive maybe
                num_input = raw_input("Please enter the subnet number you want to create: ")

                # if ( check_int(num_input) and check_network_uuid(uuid_input) ):
                if (check_int(num_input) ):
                    print 'create subnets!!'
                    manager.createSubnets(int(num_input), uuid_input)

            elif (choice == '9'):
                return

        except(KeyError):
            print "Choice Invalid"


def create():
    while True:
        print ("\n\nNETWORK Menu")
        print (">>How do you want to simulate create_network rest requests ?")
        print (">[0]: Quit Program")
        print (">[1]: List all existing network UUID")
        print (">[2]: Simulate create_network request by multiple Client:")
        print (">[9]: Back to Upper Menu")

        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if( choice == '0' ):
                quit()

            elif (choice == '1'):
                manager.list_all_networks_db()

            elif( choice == '2' ):
                data = raw_input("Please enter the client number ( 1 ~ 2500 ): ")

                if ( check_int(data) ):
                    print 'create networks!!'
                    manager.createNetworks(int(data))

            elif( choice == '9' ):
                return

        except(KeyError):
            print "Choice Invalid"



def main():
    while True:
        print ("\n\nODL_Emulator Setting Menu")
        print (">[0]: Quit Program")
        print (">[1]: List All Network UUIDs")
        print (">[2]: Create Networks")
        print (">[3]: Create Subnets")
        print (">[5]: Delete All Resourece")


        odl_menu_dict = { '0' : quit,
                          '1' : list,
                          '2' : create,
                          '3' : create_subnet,
                          '5' : del_all
                        }
        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            odl_menu_dict[choice]()

        except(KeyError):
            print "Choice Invalid!"


if __name__ == '__main__':
    main()

    # start = timeit.default_timer()
    # end = timeit.default_timer()
    # print 'All request already sent, total run time is %s second' % (end - start)
    #











