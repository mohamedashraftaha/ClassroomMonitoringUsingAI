from datetime import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from re import S
import re,boto3,os,sqlalchemy, json,secrets
from flask import Flask, jsonify, make_response,redirect, session,url_for,render_template,request
import hashlib, MySQLdb
from config.userDefinedExceptions import *
from config.s3 import access_key,secret_access_key
from boto3.session import Session
from botocore.exceptions import ClientError
from botocore.client import Config
from flask_cors import CORS, cross_origin
from flask_restx import Api, fields, Resource
from flask import Blueprint
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
from model.db_config import *
from flask_httpauth import HTTPBasicAuth
from functools import wraps
#import jwt
from datetime import timedelta

'''
This is the starting point of our backend logic for the Application.
    Our application implements an MVC architecture model, 
    where the model is the database tables and the controllers are the APIs
    and flask routes act as the view
'''


''' this is an authorization object that is used to add keys
 in the header of the API requests to protect them from
 un authorized access'''
authorizations ={
    'apikey':{
        # type of token I am expecting
		'type': 'apiKey',
		# location of the token I am expecting
		'in':'header',
		# name of the header
		'name':'X-API-KEY'		
	}
		
 
}

# configuration of the app
app=Flask(__name__)


# decorator for tokens
"""APIs Security"""



def token_required(f):
    '''@description: This function is used as a decorator
    to indicate that a certain API cannot be invoked
    without the valid token'''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # searching for the token with the title "X-API-KEY" in the request header
        # if it is available then we start processing it
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
            
        # not token is available in the request header
        # so we will return status code 401 -> Unauthorized
        if not token:
            return {'message': 'Token is missing.'}, 401
        return f(*args, **kwargs)
    return decorated


'''Here we are using Flask-restx (previusly flask-restplus) which is a library
that is used to add OpenAPI specification, i.e Swagger to our backend and thus
provide better APIs documentation'''
api = Api(
		app = app, prefix='/api',doc='/',
		version = "1.0", 
		title = "Classroom Monitoring Using AI", 
		description = "1. Used to test the APIs of the thesis project titled Classroom Monitoring Using AI\n2. Admin panel",
		authorizations=authorizations
)


'''Our APIs: are splitted into two sections:
Admin APIs and User APIs, so we created two different sections i.e namespaces'''
adminNamespace = api.namespace('admin')
userNamespace = api.namespace('user')

# get the application configuration from config.py
app.config.from_pyfile('config/config.py')

## allow server to accept requests from different sources
# so we are allowing cross origin resource sharing 
CORS(app, support_credentials=True)


# initialize database 
db = dbInit(app)
db.modelTables()

# here we create an object of type flask admin panel that
# facilitates the creation of admin panels
a = Admin(app, name='Admin Panel', url='/admin_panel')





# @app.route('/login', methods  = ['POST', 'GET'])
# def login():
# 	if request.method == 'POST':
# 		salt = request.form['password'] + app.config['SECRET_KEY']
# 		db_pass = hashlib.md5(salt.encode()).hexdigest()
# 		admin_data =  db.classroom_monitoring_db.session.query(db.admin).filter(and_(db.admin.national_id == request.form['username'], \
# 		db.admin.passwd == db_pass)).first()	
# 		token = None	
# 		if admin_data:
# 			delta = timedelta(days=3)
# 			token = jwt.encode({'user': request.form['username'],'exp' :datetime.utcnow()+delta}, app.config['SECRET_KEY'])

# 			return jsonify({'token': token.decode('UTF-8')})
# 		return make_response('Could not verify!',401,{'WWW-Authenticate': 'Basic realm="Login Required"'})
# 	return render_template('login.html')


