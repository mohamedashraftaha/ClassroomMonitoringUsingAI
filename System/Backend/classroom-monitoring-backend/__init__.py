from imports.imports import *
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

# initialize database 
db = dbInit(app)
db.modelTables()    