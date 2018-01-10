"""
Model Note
"""
import json
from DBService import getconn
from MySQLdb import MySQLError

class Note:
    """
    class Note
    """
    conn = getconn()
    cur = conn.cursor()

    def __init__(self, note_name, note_content, owner):
        """
        Note.init(note_name, note_content, owner)
        """
        self.note_name = note_name
        self.note_content = note_content
        self.owner = owner

    def insert(self):
        """
        Note.insert()
        insert notename,content,idnotebook into db
        ret:string  {'status':True,'message':'add note success'}
                    {'status':False, 'message':error.args}
        """
        try:
            sql = ("""INSERT INTO note(`notename`,`content`,`idnotebook`) VALUES(%s,%s, """
                   """(select notebookId from notebook where notebook.notebookName=%s))""")
            self.cur.execute(
                sql, (self.note_name, self.note_content, self.owner))
            self.conn.commit()
            return json.dumps({'status': True, 'message': 'add note success'})
        except MySQLError as error:
            print(error)
            self.conn.rollback()
            return json.dumps({'status': False, 'message': error.args})
    def update(self):
        """
        Note.update()
        """
        sql = ("""UPDATE note SET `content`=%s WHERE `notename`=%s and `idnotebook`=%s""")
        try:
            self.cur.execute(
                sql, (self.note_content, self.note_name, self.owner)
            )
            self.conn.commit()
            return json.dumps({'status': True, 'message': 'modify note success'})
        except MySQLError as error:
            print(error)
            self.conn.rollback()
            return json.dumps({'status': False, 'message': error.args})
        
    def delete(self):
        """Note.delete()
        """
        # DELETE FROM `cloudnote`.`note` WHERE `idnote`='00000001';
        sql = ("""DELETE FROM `cloudnote`.`note` WHERE `notename`=%s""") % (self.note_name)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return json.dumps({'status': True, 'message': 'delete note success'})
        except MySQLError as error:
            print(error)
            self.conn.rollback()
            return json.dumps({'status': False, 'message': error.args})
