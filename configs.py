HOST = 'localhost'
PORT = '3306'
DATABASE = 'awesome'
USERNAME = 'www-data'
PASSWORD = 'www-data'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
    username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

SECRET_KEY = 'aF1!fB2}cC'

