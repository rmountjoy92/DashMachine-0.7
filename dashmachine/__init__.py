import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from htmlmin.main import minify
from dashmachine.dm import DashMachine

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "66532a62c4048f976e22a39638b6f10e"

db = SQLAlchemy(app)
dm = DashMachine(app)

from dashmachine.main.routes import main

app.register_blueprint(main)

from dashmachine.source_management.sources import (
    process_local_js_sources,
    process_local_css_sources,
)


@app.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == "text/html; charset=utf-8":
        response.set_data(minify(response.get_data(as_text=True)))

        return response
    return response


@app.context_processor
def context_processor():
    return dict(
        process_local_js_sources=process_local_js_sources,
        process_local_css_sources=process_local_css_sources,
    )
