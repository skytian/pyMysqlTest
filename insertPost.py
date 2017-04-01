#!/usr/bin/python
import sys
import time
import random
import psycopg2
reload(sys)
sys.setdefaultencoding('utf-8')



config={'host':'172.0.5.202',
        'user':'hems',
        'password':'hems110',
        'port':5432,
        'database':'110'
        }
cnx = psycopg2.connect(**config)
print "Opened database successfully"

cursor = cnx.cursor()

def test():
    cnx = psycopg2.connect(**config)
    print "Opened database successfully"

def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        seconds = time.time() -start
        print "{func} operation  write {count} in {sec}s".format(func = fn.func_name, count = args[0], sec = seconds)
    return _wrapper



@time_me
def insert_cpe(count):
    for i in range(0, count):
        sql = 'delete from cpe where cpe_id = %d' % (i)
        cursor.execute(sql)
        sql = 'INSERT INTO cpe(cpe_id,serial_no, hw_id,  mme_id,   pci_range_id, cellid_range_id) VALUES (%d,1490058356%05d, 4, 1, 1, 1);' % (i, i)
        cursor.execute(sql)
    cnx.commit()


#INSERT INTO cpe(cpe_id,serial_no, hw_id,  mme_id,   pci_range_id, cellid_range_id) VALUES (3,149005835600001, 4, 1, 1, 1);



def print_info():
	print '1.insert equipment to postgres db\n'
	print '2.exit\n'

if __name__ == '__main__':
    while 1:
        test()
        print_info()
        task = raw_input("please input task:")
        if task == '1':
            loop = raw_input("insert num:")
            insert_cpe(int(loop))
        elif task == '2':
            sys.exit()
    cursor.close()
    cnx.close()
