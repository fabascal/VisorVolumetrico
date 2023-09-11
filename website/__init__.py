from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from importlib import import_module
from flask_apscheduler import APScheduler
from flask_seeder import FlaskSeeder

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
scheduler = APScheduler()
migrate = Migrate()
seeder = FlaskSeeder()

def register_extensions(app):
    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)
    
def register_blueprints(app):
    for module_name in ('authentication', 'settings', 'home'):
        module = import_module('website.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

#def configure_database(app):
#    @app.before_first_request
#    def initialize_database():
#        db.create_all()

#    @app.teardown_request
#    def shutdown_session(exception=None):
#        db.session.remove()

def add_filters(app):
    @app.template_filter('concat')
    def concat(value, arg):
        return str(value) + str(arg)

def create_app(config):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    #configure_database(app)
    add_filters(app)
    scheduler.init_app(app)
    scheduler.start()

    # Manejo de errores HTTP 500 (Internal Server Error)
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('home/error_500.html'), 500

    # Manejo de errores HTTP 404 (Página no encontrada)
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('home/page-404.html'), 404

    #Manejo de otras excepciones no capturadas
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error('Excepción no controlada: %s', (e))
        return render_template('home/error_generic.html', error_message=str(e)), 500


    return app
