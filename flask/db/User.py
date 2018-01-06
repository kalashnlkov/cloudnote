import sys
sys.path.append('./db')
import json
from DBService import getconn
from SMSService import sendSms
import random
import MySQLdb
import time

class User:
    conn = getconn()
    cur = conn.cursor()
    def __init__(self,username, telephone=None, password=None, gender=None):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.gender = gender
    def insert(self):
        try:
            #check if user exsist
            verify = self.fetchdata()
            if verify[0] is False:
                return json.dumps({'status':False, 'message':'internal error'})
            if verify[1]:
                return json.dumps({'status':False, 'message':'user exsist'})
            
            #check verifycode
            verify = self.fetchverifycode()
            if verify[0] is False:
                return json.dumps({'status':False, 'message':'verifycode internal error'})
            print(verify[1][2])
            print(self.verifycode)
            if verify[1][1] != str(self.verifycode):
                return json.dumps({'status':False, 'message':'verifycode didnot match'})
            
            sql = """INSERT INTO user(`username`,`password`,`telephone`) values(%s,%s,%s)"""
            self.cur.execute(sql,(self.username,self.password,self.telephone))
            #delete verify code
            sql = """DELETE FROM regist WHERE `username` = %s""" % (self.username)
            self.cur.execute(sql)
            self.conn.commit()
            return json.dumps({'status':True, 'message':'insert success'})
        except MySQLdb.Error as e:
            print(e)
            self.conn.rollback()
            return json.dumps({'status':False, 'message':e})
    def fetchdata(self):
        '''
        User.fetchData => (False,
        (username, userid, password, telephone,
        gender, birthday, email, city))
        '''
        data = None
        try:
            sql = """SELECT * FROM user where username='%s'"""
            self.cur.execute(sql%self.username)
            data = self.cur.fetchone()
            return (True, data)
        except MySQLdb.Error as e:
            print(e)
            return (False,data)
    def fetchverifycode(self):
        '''
        User.fetchverifycode => (True, (username,verifycode,expiretime))
        '''
        data = None
        try:
            sql = """SELECT username, verifyCode, sendTime FROM regist where username='%s'"""
            self.cur.execute(sql%self.username)
            data = self.cur.fetchone()
            return (True, data)
        except MySQLdb.Error as e:
            print(e)
            return (False,data)
    def regist(self):
        verifycode = random.randint(100000,999999)
        #sendTime format:1000-01-01 00:00:00
        #cursor.execute will format %s => '%s'
        sql = """INSERT INTO regist (`username`,`verifyCode`,`sendTime`) VALUES(%s,%s,%s)"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cur.execute(sql,(self.username,verifycode,timestamp))
            self.conn.commit()
        except MySQLdb.Error as e:
            print(e)
            self.conn.rollback()
            return False
        sendSms(self.telephone, verifycode,quiet=True)
        return True

    def destory(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print(e)
