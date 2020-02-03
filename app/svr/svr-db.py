import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Alexander29!",
    database='testdb'
)

cursor = db.cursor()
# cursor.execute("CREATE DATABASE testdb")
# cursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")
cursor.execute("SHOW TABLES")

for i in cursor:
    print(i)