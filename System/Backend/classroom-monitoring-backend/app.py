# imports all dependencies
from __init__ import *
from controllers import  userController, adminController


#this variable will be used to store passwords in the DB
salt = None

if __name__ == '__main__':

    user_level_api = userController.UserLevelAPIs()
    admin_level_api = adminController.AdminLevelAPIs()
    
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True, host='0.0.0.0')
