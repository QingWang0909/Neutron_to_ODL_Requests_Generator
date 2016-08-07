from mysql.connector import MySQLConnection, Error

from python_mysql_connect import connect


def insert_one_row(title, isbn):
    query = "INSERT INTO books(title, isbn) " \
            "VALUES(%s, %s)"
    args = (title, isbn)


    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query, args)

        if cursor.lastrowid:
            print( 'last insert id: ', cursor.lastrowid )
        else:
            print( 'last insert id not found!')

        conn.commit()   # works like Git, has to commit to database in order to make it accept changes

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def insert_multi_rows(books):
    query = "INSERT INTO books(title,isbn)" \
            "VALUES (%s, %s)"

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.executemany(query, books)

        if cursor.lastrowid:
            print('last insert id: ', cursor.lastrowid)
        else:
            print('last insert id not found!')

        conn.commit()

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()

def query_fetch_one():
    query = "SELECT * FROM books"

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query)

        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()

def iter_row(cursor, size):
    while True:
        rows = cursor.fetchmany(size)

        if not rows:
            break
        for row in rows:
            yield row

# TODO: ????
def query_fetch_many():
    query = "SELECT * FROM books"

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query)

        while True:
            rows = cursor.fetchmany(2)
            if not rows:
                break

            print (rows)

        # for row in iter_row(cursor, 2):
        #     print(row)

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()


def query_fetch_all():
    query = "SELECT * FROM books"

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        print('Total Rows: ', cursor.rowcount)
        for row in rows:
            print (row)

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()

def update_one_row(book_id, title):
    query = """UPDATE books SET title = %s WHERE id = %s"""
    data = (title, book_id)

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query, data)

        conn.commit()

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()

def delete_one_row(book_id):
    query = """DELETE FROM books WHERE id = %s"""
    data = (book_id, )

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(query, data) # arg2, which is data, must be the format that support iteration, that's why we use data = (book_id, )

        conn.commit()

    except Error as e:
        print (e)

    finally:
        cursor.close()
        conn.close()


def main():
    # insert_one_row('A Sudden Light 1', '8781439187036')

    books = [('A Sudden Light 2', '8781439187038'),
             ('A Sudden Light 3', '8781439187038'),
             ('A Sudden Light 4', '8781439187038'),
            ]

    # update_one_row(5, 'New Book')

    # insert_multi_rows(books)

    # query_fetch_one()
    # query_fetch_all()
    # query_fetch_many()

    delete_one_row(7)

if __name__ == '__main__':
    main()