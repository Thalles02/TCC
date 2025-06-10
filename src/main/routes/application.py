from flask import Blueprint, render_template, request, redirect, url_for
from src.helpers.helpers import get_ordered_table_columns
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
    # ——————————————————————————————————————————————
    # Dados fixos — precisaremos deles em GET **e** POST
    # ——————————————————————————————————————————————
    workspace = requests.post(
        url_api + "/table/list-specific-record",
        json={"token": "workspace", "record_id": id}
    ).json()['data']['records'][0]

    tabelas = requests.get(url_api + "/table/list") \
                      .json()['data']['attributes']          # todas as tabelas

    # ► 1. Tabelas que já pertencem ao workspace (sempre)
    try:
        records = requests.post(
            url_api + "/table/list-records",
            json={"token": "workspacetables",
                  "filter": {"workspace_id": id}}
        ).json()['data']['records']
    except Exception:
        records = []
        print("Não há tabelas no workspace")

    tokens_in_workspace = {rec['token_table'] for rec in records}
    list_tables_in_workspace = [t for t in tabelas if t['token'] in tokens_in_workspace]

    # ——————————————————————————————————————————————
    # POST: processa o formulário
    # ——————————————————————————————————————————————
    if request.method == "POST":
        # 2. Estados de todos os checkboxes submetidos
        dict_checkboxes = {
            t['token']: (request.form.get(f"tabelas_{t['token']}") == "on")
            for t in tabelas
        }

        # 3. Compara e sincroniza
        for token, checked in dict_checkboxes.items():
            if checked and token not in tokens_in_workspace:
                requests.post(url_api + "/table/insert-record",
                              json={"token": "workspacetables",
                                    "data": {"token_table": token,
                                             "workspace_id": id}})

            elif not checked and token in tokens_in_workspace:
                rec_id = next(r['id_workspacetables']
                              for r in records if r['token_table'] == token)
                requests.post(url_api + "/table/delete-record",
                              json={"token": "workspacetables",
                                    "record_id": rec_id})

        # Evita re‑envio duplicado
        return redirect(url_for("app_routes.workspace_management", id=id))

    return render_template(
        "workspace_management.html",
        menu_bar_active=f"workspace_{id}",
        workspace=workspace,
        workspace_id=id,
        tabelas=tabelas,
        tokens_in_workspace=tokens_in_workspace,
        list_tables_in_workspace=list_tables_in_workspace,
    )


@app_route_bp.route("/tabela/<string:token>/<int:workspace>", methods=["GET"])
def table_management(token, workspace):
    try:
        # Obtém registros
        api_resp = requests.post(
            url_api + "/table/list-records",
            json={"token": token, "filter": {}}
        ).json()
        records = api_resp["data"]["records"]
    except Exception as e:
        records = []
        print("Erro na API (records):", e)

    try:
        # Obtém atributos (metadados da tabela)
        metadata_resp = requests.post(
            url_api + "/table/list-keys",
            json={"token": token}
        ).json()
        attributes = metadata_resp["data"]["attributes"]  # [{'name': ..., 'type': ...}, ...]
    except Exception as e:
        attributes = []
        print("Erro na API (metadados):", e)

    # Extrair colunas dos dados (nome + tipo)
    all_keys_from_records = {attr['name'] for attr in attributes}
    attribute_types = {attr['name']: attr['type'] for attr in attributes}

    colunas_para_ocultar_permanentemente = {"criado_por", "atualizado_em", "atualizado_por"}
    colunas_prioritarias_pos_id = ["criado_em"]

    ordered_columns = get_ordered_table_columns(
        all_record_keys=all_keys_from_records,
        table_identifier=token,
        columns_to_hide=colunas_para_ocultar_permanentemente,
        priority_columns_after_id=colunas_prioritarias_pos_id,
        default_fallback_column_name="ID"
    )

    return render_template(
        "table_management.html",
        menu_bar_active=f"workspace_{workspace}",
        workspace_id=workspace,
        token=token,
        columns=ordered_columns,
        column_types=attribute_types,  # envia os tipos
        str_token_column=f"id_{token}".lower(),
        delete_columns=list(colunas_para_ocultar_permanentemente),
        records=records
    )