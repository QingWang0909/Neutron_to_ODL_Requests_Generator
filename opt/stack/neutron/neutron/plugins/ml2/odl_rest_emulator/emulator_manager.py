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
                self.emulator.del_network( uuid.UUID(row[2]).urn[9:] ) # convert UUID to string for northbound urlpath concatenate

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
                self.emulator.del_network( uuid.UUID(row[3]).urn[9:] ) # convert UUID to string for northbound urlpath concatenate

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
            args = (tenant_id.hex, network_id.hex, network_name)

            self.cursor.execute(mysql, args)

            self.conn.commit()

        except Error as e:
            print(e)


    def __insert_subnets_db(self, subnet_obj):
        try:
            mysql = """INSERT INTO subnets(tenant_id, subnet_name, network_id) VALUES (%s, %s, %s)"""
            args = (subnet_obj['subnet'][0]['tenant_id'], subnet_obj['subnet'][0]['name'],
                    subnet_obj['subnet'][0]['network_id'])

            self.cursor.execute(mysql, args)

            self.conn.commit()

        except Error as e:
            print(e)


    # Delete All Resources
    def delete_all_resource(self):
        self.__delete_all_ports_db()
        self.__delete_all_subnets_db()
        self.__delete_all_networks_db()


    # Generate Subnet by same network_UUID, same Tenant
    def createSubnets(self, concurrent_subnet, network_uuid):
        for i in range(concurrent_subnet):
            obj = Fake_Obj_Const.Subnet
            obj['subnet'][0]['id'] = self.__get_uuid1()
            obj['subnet'][0]['network_id'] = network_uuid

            self.__insert_subnets_db(obj)
            self.put_task_in_threads(self.emulator.create_subnet, obj)

        self.run_task_in_threads()


    # Generate Network
    #TODO: If collision happens, then delete record after raise up exception
    def createNetworks(self, concurrent_client):
        for i in range(concurrent_client):
            obj = Fake_Obj_Const.Network
            obj['network'][0]['id'] = self.__get_uuid4()
            obj['network'][0]['tenant_id'] = self.__get_uuid4()

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
if __name__ == '__main__':

    manager = EmulatorManager()

    while True:
        start = timeit.default_timer()

        cmd = str.split( raw_input('Enter Command: ') )
        if cmd[0] == 'q': print 'Emulator Program Closed' ; break

        if cmd[0] == 'c':
            print "Create Networks"
            manager.createNetworks(concurrent_num)

        if cmd[0] == 'ls':
            print "List All Networks UUID!"
            manager.list_all_networks_db()

        if cmd[0] == 'cs':
            print "Create Subnets based on given Network UUID!"
            manager.createSubnets(concurrent_num, cmd[1])

        #TODO: Parsing inputs for delete commands & UUID
        if cmd[0] == 'd':
            print "Delete networks based on UUID"
            manager.delete_One_Network('4ed65f44-5a5e-11e6-aa93-08002796ddd0')

        if cmd[0] == 'da':
            print "Delete All Resources"
            manager.delete_all_resource()

        end = timeit.default_timer()

        print 'All request already sent, total run time is %s second' %(end - start)


