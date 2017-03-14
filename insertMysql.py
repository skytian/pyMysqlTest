#!/usr/bin/python
import sys
import time
import mysql.connector
reload(sys)
sys.setdefaultencoding('utf-8')

config={'host':'localhost','user':'root','password':'casa','port':3306,'database':'hemsdb'}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        seconds = time.time() -start
        print "{func} operation  write {count} in {sec}s".format(func = fn.func_name, count = args[0], sec = seconds)
    return _wrapper

def search_user():
    query=("select name from user;")
    cursor.execute(query)
    for name in cursor:
        print name

@time_me
def insert_user(count):
    for i in range(0, count):
        sql = "insert into user(name, password, phone1, phone2, email,trueName, lockStatus, onlineStatus, oneTimePassword)values('python{}', 'pas','111111111', '1122222', '121@kdk.com', 'ti', 0, 0, 0);".format(i)
        cursor.execute(sql)
    cnx.commit()

@time_me
def transaction_insert(count):
    for i in range(0, count):
        sql = "insert into user(name, password, phone1, phone2, email,trueName, lockStatus, onlineStatus, oneTimePassword)values('python{}', 'pas','111111111', '1122222', '121@kdk.com', 'ti', 0, 0, 0);".format(i)
        cursor.execute(sql)
    cnx.commit()

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        loop = int(sys.argv[1])
        insert_user(loop)
        '''search_user()'''
        cursor.close()
        cnx.close()
    else:
        print 'error'
