from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for
from flask import request, current_app
import json


tasks = Blueprint('tasks',
                  __name__,
                  template_folder='templates',
                  static_folder='static')
htmlfile = 'task.html'

def task_template(htmlfile=None,
                  extra=None,
                  action=None,
                  node_list=None):
    return render_template(htmlfile,
                           clusters=url_for('clusters.index'),
                           nodes=url_for('nodes.index'),
                           roles=url_for('roles.index'),
                           tasks=url_for('.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           node_list=node_list,
                           data=extra) 

@tasks.route('/', endpoint='index', methods=["GET"])
def list_tasks():
    task_url = current_app.base_url + "tasks/"
    data = json.loads(current_app.build_request(task_url, "GET"))
    return task_template(htmlfile=htmlfile,
                         action='List',
                         extra=data)

@tasks.route('/create', methods=["GET","POST"])
def create_tasks():
    task_url = current_app.base_url + "tasks/"
    data = json.loads(current_app.build_request(task_url, "GET"))

    node_url = current_app.base_url + "nodes/"
    nodes = json.loads(current_app.build_request(node_url, "GET"))

    if request.method == "GET":
        return task_template(htmlfile=htmlfile,
                             action='Create',
                             node_list=nodes['nodes'],
                             extra=data)
