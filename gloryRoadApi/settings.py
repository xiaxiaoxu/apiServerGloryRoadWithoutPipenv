#encoding=utf-8
import os

project_path=os.path.dirname(os.path.dirname(__file__))
# 添加mysql数据地址mysql://用户名:密码@ip:端口/库名称
#dev_db = 'mysql://' + 'root:xiaxiaoxu@127.0.0.1:3306/api'

dbuser = 'root'
dbpassword = 'xiaxiaoxu'
dbhost = '127.0.0.1'
dbport = '3306'
dbname = 'api16'
#dev_db = 'mysql://root:xiaxiaoxu@127.0.0.1:3306/api'
dbUrl = 'mysql://' + '%s:%s@%s:%s/%s' % (dbuser, dbpassword, dbhost, dbport, dbname)

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dbUrl) # 从环境变量里取，如果没有，则用DBInitialize里的dbUrl


if __name__ == '__main__':
    print(__file__)
    print(project_path)

