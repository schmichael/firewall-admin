import os
model_path =  os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

# Use Database for application data
import sqlobject

# Connection
db_connection = sqlobject.connectionForURI('sqlite://%s/backend.db' % model_path)
sqlobject.sqlhub.processConnection = db_connection

class Users(sqlobject.SQLObject):
    username = sqlobject.StringCol(alternateID=True)
    password = sqlobject.StringCol()

class Blacklists(sqlobject.SQLObject):
    category = sqlobject.StringCol(alternateID=True)
    blacklist = sqlobject.StringCol()
    enabled = sqlobject.BoolCol()
    ips = sqlobject.StringCol()

class AllowList(sqlobject.SQLObject):
	internal = sqlobject.StringCol()
	allowlist = sqlobject.StringCol()

# Table Operations
def create_database():
    Users.createTable()
    Users(username='admin', password='admin')
    
    Blacklists.createTable()
    Blacklists(category='Default', blacklist='', enabled=True, ips='')
    
    AllowList.createTable()
