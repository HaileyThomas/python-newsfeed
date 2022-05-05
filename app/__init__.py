from flask import Flask
from app.routes import home, dashboard
from app.db import init_db
from app.utils import filters

# when flask runs the app package it will call a create_app() function


def create_app(test_config=None):
    # set up app config
    # app serves any static resources from the root directory and not from the default /static directory
    app = Flask(__name__, static_url_path='/')
    # trailing slashes are optional ie- /dashboard and /dashboard/ load the same route
    app.url_map.strict_slashes = False
    # app will use the secret key when creating server side sessions
    app.config.from_mapping(
        SECRET_KEY="super_secret_key"
    )

    # set up route
    @app.route('/hello')
    # creates inner function that returns a string
    def hello():
        return 'hello world'

    # register routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)

    # apply filters
    app.jinja_env.filters["format_url"] = filters.format_url
    app.jinja_env.filters["format_date"] = filters.format_date
    app.jinja_env.filters["format_plural"] = filters.format_plural

    # initialize database after app is ready
    init_db(app)

    return app
