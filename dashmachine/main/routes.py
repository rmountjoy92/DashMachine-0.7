from flask import Blueprint, render_template, jsonify, request
from dashmachine import dm

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    dashboard_name = request.args.get("dashboard", "main")
    return render_template(
        "main/main.html",
        dm=dm,
        dashboard_name=dashboard_name,
        title=dashboard_name if dashboard_name != "main" else None,
    )


@main.route("/load_grid", methods=["GET"])
def load_grid():
    dashboard = dm.get_dashboard_by_name(request.args.get("dashboard", "main"))
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
    return dm.main_dashboard.data_source_handler.process_data_source(
        data_source_name=request.args.get("ds")
    )
