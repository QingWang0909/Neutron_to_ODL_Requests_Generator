from rest_emulator import RestEmulator
from threading import Thread
from mock_object_template import MockObjects as Fake_Obj_Const
from connect_db import connect
from mysql.connector import MySQLConnection, Error

import sys
import timeit
import uuid
import binascii
import random


class EmulatorManager():
    def __init__(self):
        self.emulator = RestEmulator()
        try:
            self.conn = connect()
            self.cursor = self.conn.cursor(buffered=True)
        except Error as e:
            print (e)


    def statistic_all(self):
        try:
            mysql1 = """SELECT * FROM networks"""
            self.cursor.execute(mysql1)
            rows = self.cursor.fetchall()
            print ">>> Total network number currently is: " + str(self.cursor.rowcount)

            mysql2 = """SELECT * FROM subnets"""
            self.cursor.execute(mysql2)
            rows = self.cursor.fetchall()
            print ">>> Total subnet  number currently is: " + str(self.cursor.rowcount)

            mysql3 = """SELECT * FROM ports"""
            self.cursor.execute(mysql3)
            rows = self.cursor.fetchall()
            print ">>> Total port    number currently is: " + str(self.cursor.rowcount)

        except Error as e:
            print (e)


    def statistic_network(self):
        try:
            mysql1 = """SELECT * FROM networks"""
            self.cursor.execute(mysql1)
            rows = self.cursor.fetchall()
            print ">>> Total network number currently is: " + str(self.cursor.rowcount)

        except Error as e:
            print (e)


    def statistic_subnet(self):
        try:
            mysql2 = """SELECT * FROM subnets"""
            self.cursor.execute(mysql2)
            rows = self.cursor.fetchall()
            print ">>> Total subnet number currently is: " + str(self.cursor.rowcount)

        except Error as e:
            print (e)


    def statistic_port(self):
        try:
            mysql3 = """SELECT * FROM ports"""
            self.cursor.execute(mysql3)
            rows = self.cursor.fetchall()
            print ">>> Total port number currently is: " + str(self.cursor.rowcount)

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

    def __get_random_mac(self):
        mac = [random.randint(0x00, 0x7f),
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)
               ]

        return ':'.join(map(lambda x: "%02x" % x, mac))

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


    def dump_table_db(self, table):
        try:
            mysql = """SELECT * FROM """ + table

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            print('>>> Total ' + table + ' number: ' + str(self.cursor.rowcount))
            for i, row in enumerate(rows):
                if( table == 'networks' ):
                    print ">>> Network ", i + 1, " UUID: ", uuid.UUID(row[2])
                elif(table == 'subnets'):
                    print ">>> Subnet ", i + 1, " UUID: ", uuid.UUID(row[4])
                elif(table == 'ports'):
                    print ">>> Port ", i + 1, " UUID: ", uuid.UUID(row[5])

        except Error as e:
            print (e)


    def dump_resources_odl(self, resource):

        if (resource == "NETWORK"):
            self.emulator.list_networks()

        elif (resource == "SUBNET"):
            self.emulator.list_subnets()

        elif ( resource == "PORT"):
            self.emulator.list_ports()


    def dump_all_resource_odl(self):

        self.emulator.list_networks()
        self.emulator.list_ports()
        self.emulator.list_subnets()



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


    def __delete_all_ports_db(self):
        try:
            mysql = """SELECT * FROM ports"""

            self.cursor.execute(mysql)

            rows = self.cursor.fetchall()

            for row in rows:
                # Send request to ODL
                self.emulator.del_port( uuid.UUID(row[5]).urn[9:] ) # convert UUID to string for northbound urlpath concatenate

                mysql1 = """DELETE FROM ports WHERE port_id = %s"""
                args1 = (row[5], )

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


    def __insert_ports_db(self, port_obj):
        try:
            mysql = """INSERT INTO ports(tenant_id, port_name, network_id, subnet_id, port_id, mac) VALUES (%s, %s, %s, %s, %s, %s)"""
            args = ( port_obj['ports'][0]['tenant_id'], port_obj['ports'][0]['name'],
                     port_obj['ports'][0]['network_id'],port_obj['ports'][0]['fixed_ips'][0]['subnet_id'],
                     port_obj['ports'][0]['id'], port_obj['ports'][0]['mac_address'])

            self.cursor.execute(mysql, args)
            self.conn.commit()

        except Error as e:
            print(e)


    # Test if an UUID exists in Database table
    def validate_uuid(self, table, target_id, uuid_s):

        try:
            mysql = "SELECT * FROM " + table + " WHERE " + target_id + " = %s"
            args = (uuid_s, )
            self.cursor.execute(mysql, args)

            row = self.cursor.fetchall()

            if(self.cursor.rowcount == 0):
                return False
            else:
                return True

        except Error as e:
            print (e)


    # Delete All Resources
    def delete_all_resource(self, flag):
        if(flag == "ALL"):
            self.__delete_all_ports_db()
            self.__delete_all_subnets_db()
            self.__delete_all_networks_db()

        elif(flag == "NETWORK"):
            self.__delete_all_networks_db()

        elif(flag == "SUBNET"):
            self.__delete_all_subnets_db()

        elif(flag == "PORT"):
            self.__delete_all_ports_db()


    # Generate Subnet Resources
    def createSubnets(self, concurrent_subnet, network_uuid_s):
        for i in range(concurrent_subnet):
            obj = Fake_Obj_Const.Subnet

            obj['subnet'][0]['network_id'] = network_uuid_s
            obj['subnet'][0]['id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)

            # fetch tenant_id via network_id
            try:
                mysql = """select * from networks where network_id = %s"""

                args = (network_uuid_s, )

                self.cursor.execute(mysql, args)

                row = self.cursor.fetchone()
                obj['subnet'][0]['tenant_id'] = row[1]

            except Error as e:
                print (e)

            self.__insert_subnets_db(obj)
            self.put_task_in_threads(self.emulator.create_subnet, obj)

        self.run_task_in_threads()

    # Create Port Resources
    def createPorts(self, concurrent_port, subnet_uuid_s):
        for i in range(concurrent_port):
            obj = Fake_Obj_Const.Port

            obj['ports'][0]['fixed_ips'][0]['subnet_id'] = subnet_uuid_s
            obj['ports'][0]['id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)

            # fetch network_id, tenant_id via subnet_id
            try:
                mysql = """SELECT * FROM subnets WHERE subnet_id = %s"""
                args = (subnet_uuid_s, )

                self.cursor.execute(mysql, args)

                row = self.cursor.fetchone()
                obj['ports'][0]['tenant_id'] = row[1]
                obj['ports'][0]['network_id'] = row[3]
                obj['ports'][0]['mac_address'] = self.__get_random_mac()

            except Error as e:
                print (e)

            self.__insert_ports_db(obj)
            self.put_task_in_threads(self.emulator.create_port, obj)

        self.run_task_in_threads()


    # Generate Network Resources
    def createNetworks(self, concurrent_client):
        for i in range(concurrent_client):
            obj = Fake_Obj_Const.Network
            obj['network'][0]['id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)
            obj['network'][0]['tenant_id'] = self.__uuid_hex_to_string(self.__get_uuid4().hex)

            self.__insert_networks_db(obj['network'][0]['id'], obj['network'][0]['tenant_id'], obj['network'][0]['name'])
            self.put_task_in_threads(self.emulator.create_network, obj)

        self.run_task_in_threads()


    # Delete One Network
    def delete_One_Network(self, network_uuid):
        try:
            mysql = """DELETE FROM networks WHERE network_id = %s"""
            args = (network_uuid, )
            self.cursor.execute(mysql, args)
            self.conn.commit()

            # Send Request to ODL
            self.emulator.del_network(network_uuid)

        except Error as e:
            print (e)

    # Delete One Subnet
    def delete_one_Subnet(self, subnet_uuid):
        try:
            mysql = """DELETE FROM subnets WHERE subnet_id = %s"""
            args = (subnet_uuid, )
            self.cursor.execute(mysql, args)
            self.conn.commit()

            # Send Request to ODL
            self.emulator.del_subnet(subnet_uuid)

        except Error as e:
            print (e)


    # Delete One Port
    def delete_one_Port(self, port_uuid):
        try:
            mysql = """DELETE FROM ports WHERE port_id = %s"""
            args = (port_uuid, )
            self.cursor.execute(mysql, args)
            self.conn.commit()

            # Send Request to ODL
            self.emulator.del_port(port_uuid)

        except Error as e:
            print (e)


    def set_debug(self, flag):
        self.emulator.set_debug(flag)


def quit():
    print ("Program Closed! ")
    exit(1)


def del_all(flag):
    while True:
        print ("\n>>> This operation will delete all the resoureces allocated, are you sure? (Y/N) ")
        print ("[0]: No")
        print ("[1]: Yes")

        try:
            choice = raw_input("Please select a number ( 0 ~ 1 ) >> ")
            if(choice == '0'):
                return

            elif(choice == '1'):
                print ">>> delete " + flag + " resoureces!!"
                manager.delete_all_resource(flag)
                return

        except(KeyError):
            print ">>> Your input is not an integer, please enter an integer"


def debug_mode():
    while True:
        print ("\n>>> This operation will enable/disable debug mode, what would you like? ")
        print ("[0]: Disable")
        print ("[1]: Enable")

        try:
            choice = raw_input("Please select a number ( 0 ~ 1 ) >> ")
            if(choice == '0'):
                print ">>> Disable Debug Mode!!"
                manager.set_debug(False)
                return

            elif(choice == '1'):
                print ">>> Enable Debug Mode!!"
                manager.set_debug(True)
                return

        except(KeyError):
            print ">>> Your input is not an integer, please enter an integer"



def list():
    manager.statistic_all()

def retrieve_all():
    manager.dump_all_resource_odl()

def check_int(input_s):
    try:
        int(input_s)

    except ValueError:
        print (">>> Your input is *NOT* an integer, please enter an interger")
        return False

    if (int(input_s) > 0 and int(input_s) <= 2500):
        return True
    else:
        print (">>> Your input is *NOT* in a valid range, please enter an valid interger!!")
        return False


def check_uuid(input_s):
    try:
        uuid_obj = uuid.UUID(input_s)

    except:
        print (">>> Your input is *NOT* an UUID, please enter an UUID")
        return False

    return True


def port():
    while True:
        print ("\n\n[PORT Menu]")
        print (">>How do you want to simulate port rest requests ?")
        print (">[0]: Quit Program")
        print (">[1]: List all existing subnet UUID")
        print (">[2]: List all existing port UUID")
        print (">[3]: Create port via subnet UUID")
        print (">[4]: Delete one port via port UUID")
        print (">[5]: Delete all port resources")
        print (">[6]: Enable/Disable Debug Mode")
        print (">[7]: List port resources statistic")
        print (">[8]: Retrieve all port resources from ODL")
        print (">[9]: Back to Upper Menu")

        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if (choice == '0'):
                quit()

            elif (choice == '1'):
                manager.dump_table_db('subnets')

            elif (choice == '2'):
                manager.dump_table_db('ports')

            elif (choice == '3'):
                subnet_uuid = raw_input('Please enter subnet UUID number:')
                if( check_uuid(subnet_uuid) ):
                    num_input = raw_input('Please enter the number of port you want to create: ')
                    if(check_int(num_input)):
                        if(manager.validate_uuid('subnets', 'subnet_id', subnet_uuid)):
                            print '>>> create ports!!'
                            manager.createPorts(int(num_input), subnet_uuid)
                        else:
                            print '>>> UUID not exist'

            elif(choice == '4'):
                port_uuid = raw_input('Please enter port UUID number:')
                if (check_uuid(port_uuid)):
                    if(manager.validate_uuid('ports', 'port_id', port_uuid) ):
                        print ">>> delete this port!!"
                        manager.delete_one_Port(port_uuid)
                    else:
                        print '>>> UUID not exists'

            elif (choice == '5'):
                del_all("PORT")

            elif(choice == '6' ):
                debug_mode()

            elif ( choice == '7'):
                manager.statistic_port()

            elif(choice == '8'):
                manager.dump_resources_odl("PORT")

            elif (choice == '9'):
                return

        except(KeyError):
            print ">>> Choice Invalid"


def subnet():
    while True:
        print ("\n\n[SUBNET Menu]")
        print (">>How do you want to simulate subnet rest requests ?")
        print (">[0]: Quit Program")
        print (">[1]: List all existing network UUID")
        print (">[2]: List all existing subnet UUID")
        print (">[3]: Create subnets via network UUID")
        print (">[4]: Delete one subnet via subnet UUID")
        print (">[5]: Delete all subnet resources")
        print (">[6]: Enable/Disable Debug Mode")
        print (">[7]: List subnet resources statistic")
        print (">[8]: Retrieve all subnet resources from ODL")
        print (">[9]: Back to Upper Menu")


        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if (choice == '0'):
                quit()

            elif (choice == '1'):
                manager.dump_table_db('networks')

            elif (choice == '2'):
                manager.dump_table_db('subnets')

            elif (choice == '3'):
                network_uuid = raw_input("Please enter Network UUID number: ")
                if ( check_uuid(network_uuid) ):
                    num_input = raw_input("Please enter the number of subnet you want to create: ")
                    if( check_int(num_input) ):
                        if ( manager.validate_uuid('networks', 'network_id', network_uuid) ):
                            print '>>> create subnets!!'
                            manager.createSubnets(int(num_input), network_uuid)
                        else:
                            print '>>> UUID not exists'

            elif (choice == '4'):
                subnet_uuid = raw_input("Please enter Subnet UUID number: ")
                if( check_uuid(subnet_uuid)):
                    if(manager.validate_uuid('subnets', 'subnet_id', subnet_uuid)):
                        print '>>> delete this subnet!!'
                        manager.delete_one_Subnet(subnet_uuid)
                    else:
                        print '>>> UUID not exists'

            elif (choice == '5'):
                del_all("SUBNET")

            elif(choice == '6' ):
                debug_mode()

            elif (choice == '7'):
                manager.statistic_subnet()

            elif (choice == '8'):
                manager.dump_resources_odl("SUBNET")

            elif (choice == '9'):
                return

        except(KeyError):
            print ">>> Choice Invalid"


def network():
    while True:
        print ("\n\n[NETWORK Menu]")
        print (">>How do you want to simulate network rest requests ?")
        print (">[0]: Quit Program")
        print (">[1]: List all existing network UUID")
        print (">[2]: Simulate create_network request by multiple Client:")
        print (">[4]: Delete one network via network UUID")
        print (">[5]: Delete all network resources")
        print (">[6]: Enable/Disable Debug Mode")
        print (">[7]: List network resources statistic")
        print (">[8]: Retrieve all network resources from ODL")
        print (">[9]: Back to Upper Menu")

        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if( choice == '0' ):
                quit()

            elif (choice == '1'):
                manager.dump_table_db('networks')

            elif( choice == '2' ):
                data = raw_input("Please enter the client number ( 1 ~ 2500 ): ")

                if ( check_int(data) ):
                    print '>>> create networks!!'
                    manager.createNetworks(int(data))

            elif(choice == '4'):
                network_uuid = raw_input("Please enter Network UUID number: ")
                if (check_uuid(network_uuid)):
                    if (manager.validate_uuid('networks', 'network_id', network_uuid)):
                        print '>>> delete this network!!'
                        manager.delete_One_Network(network_uuid)
                    else:
                        print '>>> UUID not exists'

            elif(choice == '5'):
                del_all("NETWORK")

            elif(choice == '6' ):
                debug_mode()

            elif (choice == '7'):
                manager.statistic_network()

            elif(choice == '8'):
                manager.dump_resources_odl("NETWORK")

            elif( choice == '9' ):
                return

        except(KeyError):
            print ">>> Choice Invalid"



concurrent_num = 200
thread_pool = []
manager = EmulatorManager()

def main():
    while True:
        print ("\n\n[ODL_Emulator Setting Main Menu]")
        print (">[0]: Quit Program")
        print (">[1]: Network Menu")
        print (">[2]: Subnet Menu")
        print (">[3]: Port Menu")
        print (">[5]: Delete All Resourece")
        print (">[6]: Enable/Disable Debug Mode")
        print (">[7]: List All Resources Statistic")
        print (">[8]: Retrieve all resources from ODL")


        odl_menu_dict = { '0' : quit,
                          '1' : network,
                          '2' : subnet,
                          '3' : port,
                          '5' : del_all,
                          '6' : debug_mode,
                          '7' : list,
                          '8' : retrieve_all
                        }
        try:
            choice = raw_input("Please select a number ( 0 ~ 9 ) >> ")
            if(choice == '5'):
                odl_menu_dict[choice]("ALL")
            else:
                odl_menu_dict[choice]()

        except(KeyError):
            print ">>> Choice Invalid!"


if __name__ == '__main__':
    main()

    # start = timeit.default_timer()
    # end = timeit.default_timer()
    # print 'All request already sent, total run time is %s second' % (end - start)
    #











