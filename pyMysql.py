#!/usr/bin/python
import mysql.connector

cnx = mysql.connector.connect(user='root', password='casa',host='172.0.0.1',database='hemsdb')
cursor = cnx.cursor()
query=("select name from user;")
cursor.execute(query)
for name in cursor:
	print name
cursor.close()
cnx.close()

