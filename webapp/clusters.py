from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for
from flask import request, current_app
import json

clusters = Blueprint('clusters',
                     __name__,
                     template_folder='templates',
                     static_folder='static')
htmlfile = 'cluster.html'


def cluster_template(htmlfile=None, extra=None, action=None):
    return render_template(htmlfile,
                           clusters=url_for('.index'),
                           nodes=url_for('nodes.index'),
                           roles=url_for('roles.index'),
                           tasks=url_for('tasks.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           data=extra)


@clusters.route('/', endpoint='index', methods=["GET"])
def list_clusters():
    cluster_url = current_app.base_url + "clusters/"
    data = json.loads(current_app.build_request(cluster_url, "GET"))
    return cluster_template(htmlfile=htmlfile,
                            action='List',
                            extra=data)


@clusters.route('/<id>', methods=["GET"])
def cluster_detail(id=None):
    cluster_url = current_app.base_url + "clusters/"
    detail_url = cluster_url + id
    data = json.loads(current_app.build_request(detail_url, "GET"))
    return cluster_template(htmlfile=htmlfile,
                            action='Detail',
                            extra=data)


@clusters.route('/create', methods=["GET", "POST"])
def create_clusters():
    cluster_url = current_app.base_url + "clusters/"

    if request.method == "GET":
        return cluster_template(htmlfile=htmlfile, action='Create')

    elif request.method == "POST":
        jdata = json.dumps({"name": request.form['cluster_name'],
                            "config": 
                            json.loads(request.form['cluster_override']),
                            "description":
                            request.form['cluster_descr']}).encode('utf-8')
        current_app.build_request(cluster_url, "POST", jdata)
        return list_clusters()

    else:
        return list_clusters()


@clusters.route('/update/<id>', methods=["GET", "POST"])
def update_clusters(id=None):
    cluster_url = current_app.base_url + "clusters/"
    update_url = cluster_url + id

    if request.method == "GET":
        return cluster_template(htmlfile=htmlfile,
                                action='Update',
                                extra=json.loads(
                                current_app.build_request(update_url, "GET")))

    elif request.method == "POST":
        pprint(request.form['cluster_override'])
        jdata = json.dumps({"name": request.form['cluster_name'],
                            "config":
                            json.loads(request.form['cluster_override']),
                            "description":
                            request.form['cluster_descr']}).encode('utf-8')
        current_app.build_request(update_url, "PUT", jdata)
        return list_clusters()


@clusters.route('/delete/<id>', methods=["GET"])
def delete_clusters(id=None):
    cluster_url = current_app.base_url + "clusters/"
    delete_url = cluster_url + id

    current_app.build_request(delete_url, "DELETE")
    return list_clusters()
