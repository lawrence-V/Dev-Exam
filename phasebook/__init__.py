from flask import Flask

from . import match, search


def create_app():
    app = Flask(__name__)

    # Disable sorting of JSON keys
    app.config['JSON_SORT_KEYS'] = False

    @app.route("/")
    def hello():
        return "Hello World!"

    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)

    return app
