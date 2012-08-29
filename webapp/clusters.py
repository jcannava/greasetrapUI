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

@clusters.route('/', defaults={'list_clusters':'index'}, methods="GET")
def list_clusters():
    cluster_url = current_app.base_url + "clusters/"
    data = json.loads(current_app.build_request(cluster_url, "GET"))
    return cluster_template(htmlfile=htmlfile,
                           action='List',
                           extra=data)
clusters.add_url_rule('/', 'index', list_clusters, methods="GET")

def create_clusters():
    return cluster_template(htmlfile=htmlfile, action='Create')
clusters.add_url_rule('/create', 'create', create_clusters, methods="GET")
