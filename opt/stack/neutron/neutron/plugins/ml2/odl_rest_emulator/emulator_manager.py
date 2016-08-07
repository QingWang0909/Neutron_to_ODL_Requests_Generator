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


    def __save_networks(self, network_id, tenant_id, network_name):
        try:
            mysql = """INSERT INTO networks(tenant_id, network_id, network_name) VALUES(%s, %s, %s)"""
            args = (tenant_id.hex, network_id.hex, network_name)

            cursor = self.conn.cursor()
            cursor.execute(mysql, args)

            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()

    # Generate Network
    #TODO: If collision happens, then delete record after raise up exception
    def createNetworks(self, concurrent_client):
        for i in range(concurrent_client):
            obj = Fake_Obj_Const.Network
            obj['network'][0]['id'] = self.__get_uuid4()
            obj['network'][0]['tenant_id'] = self.__get_uuid4()

            self.__save_networks(obj['network'][0]['id'], obj['network'][0]['tenant_id'], obj['network'][0]['name'])
            self.put_task_in_threads(self.emulator.create_network, obj)

        self.run_task_in_threads()

    # Delete All Network
    #TODO: delete subnet & port first, then networks
    def delete_all_networks(self):
        try:
            mysql = """SELECT * FROM networks"""
            cursor = self.conn.cursor()

            cursor.execute(mysql)

            rows = cursor.fetchall()

            for row in rows:
                self.emulator.del_network( uuid.UUID(row[2]).urn[9:] ) # convert UUID to string for northbound urlpath concatenate
                mysql1 = """DELETE FROM networks WHERE network_id = %s"""
                args1  = (row[2], )

                cursor.execute(mysql1, args1)
                self.conn.commit()

        except Error as e:
            print (e)

        finally:
            cursor.close()

    # Delete One Network
    def delete_One_Network(self, uuid):
        self.emulator.del_network(uuid)

    # Delete One Subnet
    def delete_one_Subnet(self, uuid):
        self.emulator.del_subnet(uuid)

    # List All Networks
    def list_all_networks_db(self):
        try:
            mysql = """SELECT * FROM networks"""
            cursor = self.conn.cursor()

            cursor.execute(mysql)

            rows = cursor.fetchall()

            print('Total Network Numbers: ', cursor.rowcount)
            for i, row in enumerate(rows):
                print "Network ", i+1,  " UUID: ", uuid.UUID( row[2] )

        except Error as e:
            print (e)

        finally:
            cursor.close()


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


concurrent_num = 1000
thread_pool = []
if __name__ == '__main__':

    manager = EmulatorManager()

    while True:
        start = timeit.default_timer()

        cmd = raw_input('Enter Command: ')
        if cmd == 'q': print 'Emulator Program Closed' ; break

        if cmd == 'c':
            print "Create Networks"
            manager.createNetworks(concurrent_num)

        if cmd == 'ls':
            print "List All Networks UUID!"
            manager.list_all_networks_db()

        if cmd == 'cs':
            print "Create Subnets based on given Network UUID!"
            pass

        #TODO: Parsing inputs for delete commands & UUID
        if cmd == 'd':
            print "Delete networks based on UUID"
            manager.delete_One_Network('4ed65f44-5a5e-11e6-aa93-08002796ddd0')

        if cmd == 'da':
            print "Delete All networks"
            manager.delete_all_networks()

        end = timeit.default_timer()

        print 'All request already sent, total run time is %s second' %(end - start)


# emulator.list_security_groups()

# emulator.create_port(Fake_Obj_Const.Port)

# createSubnets(concurrent_client, '5f190e9e-5101-11e6-aa93-08002796ddd0')


# delete_One_Network( 'dccc88f6-50fd-11e6-aa93-08002796ddd0' )
# delete_one_Subnet( '43227e42-5146-11e6-aa93-08002796ddd0' )

# emulator.update_one_subnet('b262ac9a-514c-11e6-aa93-08002796ddd0', Fake_Obj_Const.Subnet)


