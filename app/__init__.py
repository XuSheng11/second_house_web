from flask import Flask
from pony.flask import Pony


def create_app():
    app = Flask(__name__)
    Pony(app=app)
    return app


app = create_app()
