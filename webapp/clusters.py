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

def list_clusters():
    cluster_url = current_app.base_url + "clusters/"
    data = json.loads(current_app.build_request(cluster_url, "GET"))
    return cluster_template(htmlfile=htmlfile,
                           action='List',
                           extra=data)
clusters.add_url_rule('/', 'index', list_clusters)
