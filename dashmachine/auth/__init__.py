import os
import toml
import logging
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user
from dashmachine.paths import users_toml, auth_cache


class Auth:
    def __init__(self, app, db, dm, user_model):
        self.dm = dm
        self.db = db
        self.app = app
        self.bcrypt = Bcrypt(self.app)
        self.user_model = user_model

        self.toml_path = users_toml
        self.error = None
        self.toml_dict = {}

        try:
            self.toml_dict = toml.load(users_toml)
        except Exception as e:
            self.error = {
                "error_title": "DashMachine was unable to read your users.toml file. \n",
                "error": f"Here is the error: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return

        self.create_users()

    def create_users(self):
        self.user_model.query.delete()
        self.db.session.commit()
        for username, opts in self.toml_dict.items():
            if opts.get("password"):
                password = self.hash_and_cache_password(
                    opts.get("password", "admin"), username
                )
            else:
                password = self.get_cached_password(username)
            user = self.user_model()
            user.username = username
            user.password = password
            user.role = opts.get("role", "admin")
            user.command_bar_visible = opts.get("command_bar_visible", True)
            self.db.session.add(user)
            self.db.session.commit()

    def hash_and_cache_password(self, password, username):
        hashed_password = self.bcrypt.generate_password_hash(password).decode("utf-8")
        with open(os.path.join(auth_cache, username), "w") as cache_file:
            cache_file.write(hashed_password)
        return hashed_password

    def get_cached_password(self, username):
        try:
            with open(os.path.join(auth_cache, username), "r") as cache_file:
                password = cache_file.read()
        except FileNotFoundError:
            return self.hash_and_cache_password("admin", username)
        return password

    def login(self, username, password, remember=False):
        user = self.user_model.query.filter_by(username=username).first()
        if not user:
            return "User not found"
        if self.bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
        else:
            return "Password is wrong"
        return "success"

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def check_dashboard_access(user, dashboard):
        if not hasattr(user, "username"):
            user.username = "anonymous"
        if not hasattr(user, "role"):
            user.role = "anonymous"

        if (
            user.username in dashboard.users_can_access
            or "all" in dashboard.users_can_access
        ):
            return True

        if (
            user.role in dashboard.roles_can_access
            or "all" in dashboard.roles_can_access
        ):
            return True

        return False
