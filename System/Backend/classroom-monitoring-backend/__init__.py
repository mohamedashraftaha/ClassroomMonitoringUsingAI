from imports.imports import *
# configuration of the app

app=Flask(__name__)
api = Api(
        app = app, 
		  version = "1.0", 
		  title = "Classroom Monitoring Using AI", 
		  description = "1. Used to test the APIs of the thesis project titled Classroom Monitoring Using AI\
                        2. Admin panel"
)
adminNamespace = api.namespace('Admin-level APIs', description='Admin Panel')
userlNameSpace = api.namespace('user-level APIs', description='Used to test user-level APIs')

app.config.from_pyfile('config/config.py')
CORS(app, support_credentials=True)
