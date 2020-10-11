import os
import logging
import uuid
from shutil import copytree, rmtree
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_caching import Cache
from dashmachine.dm import DashMachine
from dashmachine.auth import Auth
import dashmachine.paths
from dashmachine.paths import (
    config_folder,
    themes_folder,
    custom_themes_folder,
    system_themes_folder,
    static_folder,
)

logging.basicConfig(
    filename="dashmachine.log",
    filemode="w",
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

context_path = os.getenv("CONTEXT_PATH", "")
app = Flask(__name__, static_url_path=context_path + "/static")
logging.info("Flask app initialized")

cache = Cache(app, config={"CACHE_TYPE": "simple"})

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# copy bootstrap scss to config folder
config_scss_folder = os.path.join(themes_folder, "scss")
bootstrap_scss = os.path.join(static_folder, "bootstrap_scss", "scss")
if os.path.isdir(config_scss_folder):
    rmtree(config_scss_folder)
copytree(bootstrap_scss, config_scss_folder)

# copy system themes to config folder
incl_sys_themes = os.path.join(static_folder, "bootstrap_scss", "system_themes")
if os.path.isdir(system_themes_folder):
    rmtree(system_themes_folder)
copytree(incl_sys_themes, system_themes_folder)


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
login_manager = LoginManager(app)


# set up built in auth
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String())
    command_bar_visible = db.Column(db.Boolean())


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


auth = Auth(app=app, db=db, dm=dm, user_model=User)

# register blueprints
from dashmachine.main import main

app.register_blueprint(main)

# set up static context processors
from dashmachine.source_management import (
    process_local_js_sources,
    process_local_css_sources,
)


@app.context_processor
def context_processor():
    return dict(
        process_local_js_sources=process_local_js_sources,
        process_local_css_sources=process_local_css_sources,
    )
