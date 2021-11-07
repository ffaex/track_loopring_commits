# TODO add db tables
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="hashes"
)

mycursor = mydb.cursor()

sql = "CREATE TABLE hashes(id INT PRIMARY KEY AUTO_INCREMENT, hash varchar(255) UNIQUE, repo_name varchar(255));"
sql2 = "CREATE TABLE repos(id INT PRIMARY KEY AUTO_INCREMENT, repo_name varchar(255) UNIQUE);"
mycursor.execute(sql)
mycursor.execute(sql2)
mydb.commit()