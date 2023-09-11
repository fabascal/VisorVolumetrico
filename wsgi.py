from flask_migrate import Migrate
from sys import exit
from decouple import config

from website.config import config_dict
from website import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
    
app = create_app(app_config)
app_ctx = app.app_context()
app_ctx.push()
Migrate(app, db)

from website.home import models
from website.authentication import models
from website.settings import models

print("DEBUG Value:", DEBUG)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
app.debug = True
if __name__ == "__main__":
    app.run(debug=True)
