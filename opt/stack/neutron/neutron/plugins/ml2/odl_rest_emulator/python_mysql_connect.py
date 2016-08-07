import mysql.connector
from mysql.connector import Error

def connect():
    """ Connect to MySQL database """

    try:
        conn = mysql.connector.connect(host = 'localhost',
                                       database = 'test',
                                       user = 'root',
                                       password = 'admin'
                                       )

        if conn.is_connected():
            print('Connected to MySQL database!')

        return conn

    except Error as e:
        print(e)

    finally:
        pass
        # conn.close()  # Only close MySQL connection after it no longer used

if __name__ == '__main__':
    connect()