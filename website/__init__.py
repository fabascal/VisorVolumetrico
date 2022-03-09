from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from importlib import import_module
from flask_apscheduler import APScheduler

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
scheduler = APScheduler()
migrate = Migrate()


def register_extensions(app):
    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
def register_blueprints(app):
    for module_name in ('authentication','settings','home'):
        module = import_module('website.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    
    @app.before_first_request
    def initialize_database():
        db.create_all()        

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()



def create_app(config):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(config) 
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    scheduler.init_app(app)
    scheduler.start()
    return app
    
    


