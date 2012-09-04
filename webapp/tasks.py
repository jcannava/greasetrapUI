from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

tasks = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')
htmlfile = 'task.html'

def task_template(htmlfile=None, extra=None, action=None):
    return render_template(htmlfile,
                           clusters=url_for('clusters.index'),
                           nodes=url_for('nodes.index'),
                           roles=url_for('roles.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           data=extra) 

@tasks.route('/', endpoint='index', methods=["GET"])
def list_tasks():
    task_url = current_app.base_url + "tasks/"
    data = json.loads(current_app.build_request(task_url, "GET"))
    return task_template(htmlfile=htmlfile,
                         action='List',
                         extra=data)
