import unittest
import pandas as pd
import unittest
import psycopg2
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine


# Import data
data = pd.read_csv("Codes/data/global_tab.csv")

#Columns name
cols = ['Code', 'Country', 'Study', 'Tag', 'Created', 'Submission', 'Documents', 'Note']

# create engine to connect into databases
engine = create_engine('mysql://root:mdclinicals@localhost/linh')

# function to test databases
def db_read(query, params=None):
    try:
        cnx = engine.raw_connection()
        cursor = cnx.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        entries = cursor.fetchall()

        content = []
        for entry in entries:
            content.append(entry)

        return content

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User authorization error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        else:
            print(err)

    finally:
        cursor.close()
        cnx.close()
        print("Connection closed")

res = db_read("select * from Documents")
print(db_read("Select VERSION()") == [('8.0.28',)])

'''

# class with all functions we want to test
class TestImportInsert(unittest.TestCase):

    def test_import(self):
        assert data.shape == (2274, 8)

        self.assertIn('Code', data.columns)
        self.assertIn('Country', data.columns)
        self.assertIn('Study', data.columns)
        self.assertIn('Tag', data.columns)
        self.assertIn('Created', data.columns)
        self.assertIn('Submission', data.columns)
        self.assertIn('Documents', data.columns)
        self.assertIn('Note', data.columns)


    def test_connexion(self):
        assert len(res) == 2274



if __name__ == '__main__':
    unittest.main()'''