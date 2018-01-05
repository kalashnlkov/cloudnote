import sys
sys.path.append('./db')
from DBService import getconn
from SMSService import sendSms
import random
import MySQLdb
import time

class User:
    conn = getconn()
    cur = conn.cursor()
    def __init__(self,username, telephone, password=None, gender=None):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.gender = gender
    def insert(self):
        try:
            sql = """INSERT INTO user(`username`,`password`,`telephone`,`gender`) values('%s','%s','%s','%s')"""
            print(self.cur.execute(sql%(self.username, self.password, self.telephone, self.gender)))
            self.conn.commit()
            print('user.insert success')
        except:
            self.conn.rollback()
            print('user.insert error happen')
    def fiter(self):
        try:
            sql = """INSERT INTO user(`username`,`password`,`telephone`,`gender`) values(%s,%s,%s,%s)"""
            print(self.cur.execute(sql, self.username, self.password, self.telephone, self.gender))
            self.conn.commit()
            print('user.insert success')
        except:
            self.conn.rollback()
            print('user.insert error happen')
    def regist(self):
        verifyCode = random.randint(100000,999999)
        #sendTime format:1000-01-01 00:00:00
        #cursor.execute will format %s => '%s'
        sql = """INSERT INTO regist (`username`,`verifyCode`,`sendTime`) VALUES(%s,%s,%s)"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cur.execute(sql,(self.username,verifyCode,timestamp))
            self.conn.commit()
        except MySQLdb.Error as e:
            print(e)
            self.conn.rollback()
            return False
        sendSms(self.telephone, verifyCode,quiet=True)
        return True

    def destory(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print(e)
