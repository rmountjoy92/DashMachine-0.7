from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from htmlmin.main import minify
from dashmachine.dm import DashMachine

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "66532a62c4048f976e22a39638b6f10e"

db = SQLAlchemy(app)

dm = DashMachine(app)
if dm.error:
    raise Exception(dm.error)

from dashmachine.main.routes import main

app.register_blueprint(main)

from dashmachine.source_management import sources


@app.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == "text/html; charset=utf-8":
        response.set_data(minify(response.get_data(as_text=True)))

        return response
    return response
