import pandas as pd
import sqlalchemy
import pymysql

file_name = r'C:\Shalu\LiveProjects\swiggy_instamart_bakeryfood\input_files\pin.xlsx'
df = pd.read_excel(file_name)
mydb = pymysql.connect(host="localhost", user="root", password="actowiz", database="swiggy_instamart_bakeryfood")
cur = mydb.cursor()
table_name = "pin"
db_conn = sqlalchemy.create_engine("mysql+pymysql://root:actowiz@localhost/swiggy_instamart_bakeryfood")
df.to_sql(table_name, con=db_conn, if_exists='replace', index=False)
mydb.commit()
print("file inserted to data base")