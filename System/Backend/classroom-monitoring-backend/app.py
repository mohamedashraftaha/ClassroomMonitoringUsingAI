# imports all dependencies
from __init__ import *
from model.db_config import *
from controllers.adminController import  *
from controllers.userController import *

#this variable will be used to store passwords in the DB
salt = None
    # initialize database 
db = dbInit(app)
db.modelTables()
if __name__ == '__main__':
    admin_level_api = AdminLevelAPIs()
    user_level_api = UserLevelAPIs()
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)
