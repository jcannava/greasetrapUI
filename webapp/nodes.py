from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

clusters = Blueprint('nodes', __name__, template_folder='templates', static_folder='static')
htmlfile = 'node.html'

def node_template(htmlfile=None, extra=None, action=None, cluster_data=None, role_data=None):
    return render_template(htmlfile,
                           nodes=url_for('.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           data=extra,
                           cluster_list=cluster_data,
                           role_list=role_data) 
