from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

roles = Blueprint('roles', __name__, template_folder='templates', static_folder='static')
htmlfile = 'role.html'

def role_template(htmlfile=None, extra=None, action=None):
    return render_template(htmlfile,
                           clusters=url_for('clusters.index'),
                           nodes=url_for('nodes.index'),
                           roles=url_for('.index'),
                           css=url_for('.static', filename='site.css'),
                           action=action,
                           data=extra)

@roles.route('/', endpoint='index', methods=["GET"])
def list_roles():
    role_url = current_app.base_url + "roles/"
    data = json.loads(current_app.build_request(role_url, "GET"))
    return role_template(htmlfile=htmlfile,
                         action='List',
                         extra=json.loads(current_app.build_request(role_url, "GET")))

@roles.route('/create', methods=["GET", "POST"])
def create_roles():
    role_url = current_app.base_url + "roles/"
    
    if request.method == "GET":
        return role_template(htmlfile=htmlfile, action='Create')

    elif request.method == "POST":
        jdata = json.dumps({"name": request.form['role_name'],
                            "description": request.form['role_descr']}).encode('utf-8')
        current_app.build_request(role_url, "POST", jdata)
        return list_roles()

@roles.route('/update/<id>', methods=["GET", "POST"])
def update_roles(id=None):
    role_url = current_app.base_url + "roles/"
    update_url = role_url + id

    if request.method == "GET":
        return role_template(htmlfile=htmlfile, 
                             action='Update',
                             extra=json.loads(current_app.build_request(update_url, "GET")))

    elif request.method == "POST":
        jdata = json.dumps({"name": request.form['role_name'],
                            "description": request.form['role_descr']}).encode('utf-8')
        current_app.build_request(update_url, "PUT", jdata)
        return list_roles()

@roles.route('/delete/<id>', methods=["GET"])
def delete_roles(id=None):
    role_url = current_app.base_url + "roles/"
    delete_url = role_url + id

    current_app.build_request(delete_url, "DELETE")
    return list_roles()
