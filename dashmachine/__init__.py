import os
import logging
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from htmlmin.main import minify
from dashmachine.dm import DashMachine
from dashmachine.paths import config_folder

logging.basicConfig(
    filename="dashmachine.log",
    filemode="w",
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

app = Flask(__name__)
logging.info("Flask app initialized")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Generate secret key
secret_file = os.path.join(config_folder, ".secret")
if not os.path.isfile(secret_file):
    with open(secret_file, "w") as new_file:
        new_file.write(uuid.uuid4().hex)
        logging.info(f"Generated new .secret file at {secret_file}")
with open(secret_file, "r") as file:
    secret_key = file.read().encode("utf-8")
    if len(secret_key) < 32:
        secret_key = uuid.uuid4().hex
        logging.warning(
            f"Secret in {secret_file} is less than 32 chars. "
            f"Generating a new one. You will constantly have to "
            f"log in until you fix this."
        )
app.config["SECRET_KEY"] = secret_key
logging.info(f"Set secret key using {secret_file}")

db = SQLAlchemy(app)
dm = DashMachine(app)

from dashmachine.main.routes import main

app.register_blueprint(main)

from dashmachine.source_management import (
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
