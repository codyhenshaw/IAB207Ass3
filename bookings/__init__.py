from os import path
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
app=Flask(__name__)
DB_NAME = "database.db"

def create_app():
    
    #we use this utility module to display forms quickly
    bootstrap = Bootstrap(app)

    #A secret key for the session object
    app.secret_key='somerandomvalue'

    #Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import bookings
    app.register_blueprint(bookings.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')
    

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("404.html")