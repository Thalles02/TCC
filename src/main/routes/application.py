from flask import Blueprint, render_template, request, redirect
import requests

app_route_bp = Blueprint("app_routes", __name__)

url_api = "http://127.0.0.1:5000"

@app_route_bp.context_processor
def inject_global_variables():
    workspaces = (requests.get(url_api + "/workspace/list")).json()['data']['attributes']
    return dict(
        workspaces=workspaces,
    )


@app_route_bp.route("/inicio", methods=["GET", "POST"])
def homepage():
    menu_bar_active = "inicio"

    if request.method == "POST":
        workspace_name = request.form.get("workspace")

        response = requests.post(url_api + "/workspace/register", json={"name": workspace_name})

        return redirect("/inicio")


    return render_template(
        'homepage.html', 
        menu_bar_active=menu_bar_active
    )

@app_route_bp.route("/workspace/<int:id>", methods=["GET", "POST"])
def workspace_management(id):

    workspace = requests.post(url_api + "/table/list-specific-record", json={"token": "workspace", "record_id": (id)})
    workspace = (workspace.json())['data']['records'][0]

    tabelas = requests.get(url_api + "/table/list").json()['data']['attributes']




    return render_template(
        'workspace_management.html', 
        menu_bar_active=f"workspace_{id}",
        workspace=workspace,
        tabelas=tabelas,
    )