from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from re import S
import re,boto3,os,sqlalchemy, json,secrets
from flask import Flask, jsonify,redirect, session,url_for,render_template,request
import hashlib, MySQLdb
from config.userDefinedExceptions import *
from config.s3 import access_key,secret_access_key
from boto3.session import Session
from botocore.exceptions import ClientError
from botocore.client import Config
from flask_cors import CORS, cross_origin
from flask_restx import Api, fields, Resource
from flask import Blueprint
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
from model.db_config import *
# configuration of the app

app=Flask(__name__)
api = Api(
        app = app, 
		  version = "1.0", 
		  title = "Classroom Monitoring Using AI", 
		  description = "1. Used to test the APIs of the thesis project titled Classroom Monitoring Using AI\n2. Admin panel"
)
adminNamespace = api.namespace('api/admin')
userNamespace = api.namespace('api/user')

app.config.from_pyfile('config/config.py')
CORS(app, support_credentials=True)


a = Admin(app, url = '/admin')
# initialize database 
db = dbInit(app)
db.modelTables()    
