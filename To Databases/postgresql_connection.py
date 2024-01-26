import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='', 
    user='', 
    password='', 
    port=, 
    database='')

consulta_sql = pd.read_sql_query('''

''', conn)