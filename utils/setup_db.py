import sqlite3
import os
import sys

'''
creates a test database for this web project
'''


# sqlite database
db_path_rel = '../db'
db_name = 'blog.sqlite3'
db_file_rel = os.path.join(db_path_rel, db_name)
db_table = 'posts'


if os.path.exists(db_file_rel ):
    print("EXITING: Database", db_file_rel, "exists.")
    sys.exit(0)


# create a new database if the database doesn't already exist
with sqlite3.connect(db_file_rel) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    print("Creating database ... ", db_name)

    try:
        # create the table
        print("Creating table ... ", db_table)
        c.execute("""CREATE TABLE {}(title TEXT, post TEXT)""".format(db_table))

        # insert dummy data into the table
        c.execute('INSERT INTO {} VALUES("Good", "I\'m good.")'.format(db_table))
        c.execute('INSERT INTO {} VALUES("Well", "I\'m well.")'.format(db_table))
        c.execute('INSERT INTO {} VALUES("Excellent", "I\'m excellent.")'.format(db_table))
        c.execute('INSERT INTO {} VALUES("Okay", "I\'m okay.")'.format(db_table))

    except sqlite3.OperationalError as e:
                print("FATAL ERROR:", e.args[0])
