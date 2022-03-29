import unittest
import pandas as pd
import unittest
import psycopg2
import mysql.connector

# Import data
data = pd.read_csv("Codes/data/global_tab.csv")

#Columns name
cols = ['Code', 'Country', 'Study', 'Tag', 'Created', 'Submission', 'Documents', 'Note']


"""
conn_mysql = mysql.connector.connect(host="localhost",
                        user="root",
                        password="mdclinicals",
                        database="linh")
first_val = "('AT', 'Austria', 'Pre-Market', 1.0, '2022-03-14', 'Competent Authority', 'Application Form ', 'Download from webpage: https://applicationform.basg.gv.at/mpgform/faces/main. In PDF (signed electronically or scanned signed original) and XML ')"
"""

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

  


if __name__ == '__main__':
    unittest.main()