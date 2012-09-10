from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for
from flask import request, current_app
import json

nodes = Blueprint('nodes',
                  __name__,
                  template_folder='templates',
                  static_folder='static')
htmlfile = 'node.html'


def node_template(htmlfile=None,
                  extra=None,
                  action=None,
                  cluster_data=None,
                  role_data=None):
    return render_template(htmlfile,
                           clusters=url_for('clusters.index'),
                           nodes=url_for('.index'),
                           roles=url_for('roles.index'),
                           tasks=url_for('tasks.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           data=extra,
                           cluster_list=cluster_data,
                           role_list=role_data)


@nodes.route('/', endpoint='index', methods=["GET"])
def list_nodes():
    node_url = current_app.base_url + "nodes/"
    data = json.loads(current_app.build_request(node_url, "GET"))
    return node_template(htmlfile=htmlfile,
                         action='List',
                         extra=json.loads(
                         current_app.build_request(node_url, "GET")))


@nodes.route('/create', methods=["GET", "POST"])
def create_nodes():
    node_url = current_app.base_url + "nodes/"

    cluster_url = current_app.base_url + "clusters/"
    role_url = current_app.base_url + "roles/"

    cluster_data = json.loads(current_app.build_request(cluster_url, "GET"))
    role_data = json.loads(current_app.build_request(role_url, "GET"))

    if request.method == "GET":
        return node_template(htmlfile=htmlfile,
                             action='Create',
                             cluster_data=cluster_data,
                             role_data=role_data)

    elif request.method == "POST":
        jdata = json.dumps({"hostname": request.form['hostname'],
                            "cluster_id": request.form['cluster'],
                            "role_id": request.form['role']}).encode('utf-8')
        current_app.build_request(node_url, "POST", jdata)
        return list_nodes()


@nodes.route('/update/<id>', methods=["GET", "POST"])
def update_nodes(id=None):
    node_url = current_app.base_url + "nodes/"
    update_url = node_url + id

    cluster_url = current_app.base_url + "clusters/"
    role_url = current_app.base_url + "roles/"

    cluster_data = json.loads(current_app.build_request(cluster_url, "GET"))
    role_data = json.loads(current_app.build_request(role_url, "GET"))

    if request.method == "GET":
        data = json.loads(current_app.build_request(update_url, "GET"))
        return node_template(htmlfile=htmlfile,
                             action='Update',
                             extra=data,
                             cluster_data=cluster_data,
                             role_data=role_data)

    elif request.method == "POST":
        jdata = json.dumps({"hostname": request.form['hostname'],
                            "cluster_id": request.form['cluster'],
                            "role_id": request.form['role']}).encode('utf-8')
        current_app.build_request(update_url, "PUT", jdata)
        return list_nodes()


@nodes.route('/delete/<id>', methods=["GET"])
def delete_nodes(id=None):
    node_url = current_app.base_url + "nodes/"
    delete_url = node_url + id
    current_app.build_request(delete_url, "DELETE")
    return list_nodes()
