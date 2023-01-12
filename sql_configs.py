from configs import mode
HOST = 'localhost'
PORT = '3306'
DATABASE = 'awesome'
USERNAME = 'www-data'
PASSWORD = 'www-data'
'''
设置mysql host为localhost(本机)
port为3306(mysql默认)
数据库名为awesome
用户名为www-data
密码为www-data
'''
DB_URI = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
    username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
# 连接数据库
if mode == 'dev':
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 追踪对象的修改并且发送信号
    SQLALCHEMY_ECHO = True
    # 是否打印mysql执行的语句
SECRET_KEY = 'aF1!fB2}cC'
# session key值，自用于session加密，可以随意修改
