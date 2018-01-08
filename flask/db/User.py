import sys
sys.path.append('./db')
import json
from DBService import getconn
from SMSService import sendSms
import random
import MySQLdb
import time

class User:
    verifycode = None
    conn = getconn()
    cur = conn.cursor()

    def __init__(self,username, telephone=None, password=None, gender=None):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.gender = gender
    def insert(self, update=False):
        """
        User.insert(self, sql=None)
        do insert new user when update=False
        do update user instead
        """
        try:
            #check if user exsist
            verify = self.fetchdata()
            if verify['status'] is False:
                return json.dumps({'status':False, 'message':'internal error'})
            if verify['message']:
                return json.dumps({'status':False, 'message':'user exsist'})
            
            #check verifycode
            verify = self.fetchverifycode()
            if verify['status'] is False:
                return json.dumps({'status':False, 'message':'verifycode internal error'})
            print(verify)
            print(self.verifycode)
            if verify['message']['verifyCode'] != str(self.verifycode):
                return json.dumps({'status':False, 'message':'verifycode didnot match'})
            if update:
            #TODO update
                sql = """UPDATE user set password=%s where username=%s"""
                self.cur.execute(sql, (user.password, self.username))
            else
                sql = """INSERT INTO user(`username`,`password`,`telephone`) values(%s,%s,%s)"""
                self.cur.execute(sql, (self.username, self.password, self.telephone))
                
            #delete verify code
            sql = """DELETE FROM regist WHERE `username` = '%s'""" % (self.username)
            self.cur.execute(sql)
            self.conn.commit()
            return json.dumps({'status':True, 'message':'insert success'})
        except MySQLdb.Error as e:
            #TODO mysql_exceptions get content [all try/except]
            print(e)
            e = 'internal error'
            self.conn.rollback()
            return json.dumps({'status':False, 'message':e})
            
    def update(self)
        ret = user.insert(self, True)
        return ret
        
    def login(self):
        ret = self.fetchdata()
        if not (ret['status'] and ret['message']):
            return {'status':False,
                    'message':'status:%s not such user '%ret['status']}
        ret = ret['message']
        if self.username == ret['username'] and \
            self.password == ret['password']:
            return {'status':True,
                    'message':'login success'}
        return {'status':False,
                'message':'error password'}

    def fetchdata(self):
        '''
        User.fetchData => {'status':True, 'message':result}
        '''
        try:
            sql = """SELECT * FROM user where username='%s'"""
            self.cur.execute(sql%self.username)
            result = self.dictfetchall()
            return {'status':True,'message':result}
        except MySQLdb.Error as e:
            print(e)
            e = 'internal error'
            return {'status':False,'message':e}
    def fetchverifycode(self):
        '''
        User.fetchverifycode => {'status':True, 'message':result}
                            result => dict about username verifyCode sendTime
        '''
        try:
            sql = """SELECT username, verifyCode, sendTime FROM regist where username='%s'"""
            self.cur.execute(sql%self.username)
            result = self.dictfetchall()
            return {'status':True,'message':result}
        except MySQLdb.Error as e:
            print(e)
            e = 'internal error'
            return {'status':False,'message':e}
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
            e = 'internam error'
            self.conn.rollback()
            return {'status':False, 'message':e}
        sendSms(self.telephone, verifycode,quiet=True)
        return {'status':True, 'message':'send sms success'}

    def destory(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print(e)
    #MySQL return tuple to json
    def dictfetchall(self):
        """Returns all rows from a cursor as a list of dicts"""
        desc = self.cur.description
        ret = [dict(zip([col[0] for col in desc], row))
                for row in self.cur.fetchall()]
        if not ret:
            return []
        return ret[0]