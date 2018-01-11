# -*- coding=utf-8 -*-
from app import create_app, db
from app.models import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 设置 mysqlbd 来连接 mysql
import pymysql
pymysql.install_as_MySQLdb()

# 创建app，并配置。
# 配置选项可查看 config.py 文件
app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)  # registe migrate to flask

manager.add_command('db', MigrateCommand)   # use db for shell environment

@manager.shell
def make_shell_context():
    return dict(app=app, db=db,User=User,Note=Note,
                Notebook=Notebook,
                Auth=Auth)

if __name__ == '__main__':
    manager.run()
