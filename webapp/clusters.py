from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

clusters = Blueprint('clusters', __name__, template_folder='templates', static_folder='static')
htmlfile = 'cluster.html'

def cluster_template(htmlfile=None, extra=None, action=None, data=None):
    return render_template(htmlfile,
                           clusters=url_for('.index'),
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

# TODO: Template and route for cluster details
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
                            "description": request.form['cluster_descr']}).encode('utf-8')
        current_app.build_request(cluster_url, "POST", jdata)
        data = json.loads(current_app.build_request(cluster_url, "GET"))
        return cluster_template(htmlfile=htmlfile,
                                action='List',
                                extra=data)
    else:
        return cluster_template(htmlfile=htmlfile, action='List')

@clusters.route('/update/<id>', methods=["GET", "POST"])
def update_clusters(id=None):
    cluster_url = current_app.base_url + "clusters/"
    update_url = cluster_url + id

    if request.method == "GET":
        return cluster_template(htmlfile=htmlfile,
                                action='Update',
                                extra=json.loads(current_app.build_request(update_url, "GET")))

    elif request.method == "POST":
        jdata = json.dumps({"name": request.form['cluster_name'],
                            "description": request.form['cluster_descr']}).encode('utf-8')
        current_app.build_request(update_url, "PUT", jdata)
        data = json.loads(current_app.build_request(cluster_url, "GET"))
        return cluster_template(htmlfile=htmlfile,
                                action='List',
                                extra=data)

@clusters.route('/delete/<id>', methods=["GET"])
def delete_clusters(id=None):
    cluster_url = current_app.base_url + "clusters/"
    delete_url = cluster_url + id
   
    current_app.build_request(delete_url, "DELETE")
    data = json.loads(current_app.build_request(cluster_url, "GET"))
    return cluster_template(htmlfile=htmlfile,
                            action='List',
                            extra=data)
