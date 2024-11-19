from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import pymysql

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
jwt = JWTManager()
