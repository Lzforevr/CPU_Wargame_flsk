# 配置
# 数据库的配置信息

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'cpu_wargame'
USERNAME = 'root'
PASSWORD = "6666"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4' \
    .format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = False
MAIL_PORT = 587
MAIL_USERNAME = '1446219282@qq.com'
MAIL_PASSWORD = 'djvmixsoedukbagb'
MAIL_DEFAULT_SENDER = '1446219282@qq.com'

# session的盐加密
SECRET_KEY = 'hfaiehfjieohf'