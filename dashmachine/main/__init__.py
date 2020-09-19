from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import current_user
from htmlmin.main import minify
from dashmachine import dm, auth

main = Blueprint("main", __name__)


@main.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == "text/html; charset=utf-8":
        response.set_data(minify(response.get_data(as_text=True)))

        return response
    return response


@main.route("/", methods=["GET"])
def index():
    if dm.settings.login_required and not current_user.is_authenticated:
        return redirect(url_for("main.login"))

    dashboard_name = request.args.get("dashboard", "main")
    return render_template(
        "main/main.html",
        dm=dm,
        dashboard_name=dashboard_name,
        tags=request.args.get("tags").split(",") if request.args.get("tags") else [],
        title=dashboard_name if dashboard_name != "main" else None,
    )


@main.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("user_system/login.html", dm=dm)


@main.route("/check_login", methods=["POST"])
def check_login():
    resp = auth.login(
        username=request.form.get("username"),
        password=request.form.get("password"),
        remember=request.form.get("remember"),
    )
    return resp


@main.route("/logout", methods=["GET"])
def logout():
    auth.logout()
    return redirect(url_for("main.login"))


@main.route("/load_grid", methods=["GET"])
def load_grid():
    dashboard = dm.get_dashboard_by_name(request.args.get("dashboard"))
    if not dashboard:
        dashboard = dm.get_dashboard_by_name("main")
    if dashboard.error:
        return jsonify(
            data={
                "error": dashboard.error["error"],
                "error_title": dashboard.error["error_title"],
            }
        )

    return render_template("main/dashboard.html", dashboard=dashboard)


@main.route("/load_data_source", methods=["GET"])
def load_data_source():
    return dm.data_source_handler.process_data_source(
        data_source_name=request.args.get("ds")
    )


@main.route("/get_logs", methods=["GET"])
def get_logs():
    return dm.get_logs()


@main.route("/change_theme", methods=["GET"])
def change_theme():
    dm.change_theme(request.args.get("theme_name", "default_light"))
    return "ok"
