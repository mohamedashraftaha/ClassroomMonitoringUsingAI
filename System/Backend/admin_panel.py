# imports all dependencies
from flask import abort, make_response
from __init__ import *
"""Admin panel creation"""


'''Part1:
in this part we are creating the security for the admin panel
to make sure that no one can access the admin panel except for the users'''

# using http basic auth library in flask that maintain the authorization
# to roures
auth = HTTPBasicAuth()
@app.route('/admin/')
@auth.login_required
def authorization():
	return redirect('/admin_panel')

@auth.verify_password
def authenticate(username, password):
    '''@description: this function is responsible for authenticating the
    user, making sure that this user is registered as an admin in the database'''
    
    salt = password + app.config['SECRET_KEY']
    
    db_pass = hashlib.md5(salt.encode()).hexdigest()
    
    admin_data =  db.classroom_monitoring_db.session.query(db.admin).filter(and_(db.admin.national_id == username, \
    
    db.admin.passwd == db_pass)).first()
    
    if admin_data is None:
        return False
    
    else:

        session['logged_in'] = True
        return redirect("/admin_panel")   


'''Part2 : creating a class that represents the view by which the 
database table will be displayed'''
class MyModelView(ModelView):
    column_display_pk = True
  
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)
    def __repr__(self) -> str:
        return super().__repr__()
    def is_accessible(self):
        
        if "logged_in" in session:            
            return True
        else:
            abort(403)


