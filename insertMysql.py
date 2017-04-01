#!/usr/bin/python
import sys
import time
import random
import mysql.connector
reload(sys)
sys.setdefaultencoding('utf-8')

config={'host':'localhost',
        'user':'root',
        'password':'casa',
        'port':3306,
        'database':'hemsdb',
        'autocommit':'true'}
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
    '''cnx.commit()'''

@time_me
def transaction_insert_user(count):
    cnx.start_transaction()
    for i in range(0, count):
        sql = "insert into user(name, password, phone1, phone2, email,trueName, lockStatus, onlineStatus, oneTimePassword)values('db_test_user_{}', 'pas','111111111', '112222233', 'db_test_user_{}@casa.com', 'true_name_{}', 0, 0, 0);".format(i, i, i)
        cursor.execute(sql)
    cnx.commit()

def delete_user():
    sql = "delete from user where name like 'db_test_user_%';"
    cursor.execute(sql)
    cnx.commit()

@time_me
def transaction_insert_usergroup(count):
    cnx.start_transaction()
    for i in range(0, count):
        sql = "insert into usergroup(name, creator, description)values('db_test_usergroup_{}', 'db_test_creator_{}','test descriptionn {}');".format(i, i, i)
        cursor.execute(sql)
    cnx.commit()


@time_me
def transaction_insert_authority(count):
    cnx.start_transaction()
    for i in range(0, count):
        sql = "select id from user where name = 'db_test_user_{}'".format(i);
        cursor.execute(sql)
        uid =  cursor.fetchone()
        sql = "select id from usergroup where name = 'db_test_usergroup_{}'".format(random.randint(0, 199))
        cursor.execute(sql)
        gid = cursor.fetchone()
        sql = "insert into authority(userId, userGroupId) values({},{})".format(uid[0], gid[0])
        cursor.execute(sql)
    cnx.commit()



@time_me
def insert_eq_and_ne(count):
    cnx.start_transaction()
    for i in range(0, count):
        sql = "select id from user where name = 'db_test_user_{}'".format(random.randint(0, 1999))
        cursor.execute(sql)
        uid =  cursor.fetchone()
        sql = "insert into equipment(OUI, num, name, typeId, location, creatorid) values('8%05d', '172767%05d', 'db_test_eq_%d', '%d', 'tianhe', '%d')" % (random.randint(0, 100), i, i, random.randint(1,3), uid[0]);
        cursor.execute(sql)
    cnx.commit()
    cnx.start_transaction()
    for i in range(0, count):
        sql = "select id from equipment where name = 'db_test_eq_{}'".format(i)
        cursor.execute(sql)
        eid =  cursor.fetchone()
        sql = "insert into ne(equipmentid, name, typeId) values(%d, 'db_test_ne_%d', %d)" % (int(eid[0]), i, 5)
        cursor.execute(sql)
    cnx.commit()


def print_info():
	print '1.insert user to db\n'
	print '2.insert usergroup to db\n'
	print '3.insert authority to db\n'
	print '4.delete user\n'
        print '5.insert equipment and ne to db\n'
	print '10.exit\n'

if __name__ == '__main__':
    while 1:
        print_info()
        task = raw_input("please input task:")
        if task == '1':
            loop = raw_input("insert num:")
            transaction_insert_user(int(loop))
        elif task == '2':
            loop = raw_input("insert num:")
            transaction_insert_usergroup(int(loop))
        elif task == '3':
            loop = raw_input("insert num:")
            transaction_insert_authority(int(loop))
        elif task == '4':
            delete_user()
        elif task == '5':
            loop = raw_input("insert num:")
            insert_eq_and_ne(int(loop))
        elif task == '10':
            sys.exit()
    cursor.close()
    cnx.close()
