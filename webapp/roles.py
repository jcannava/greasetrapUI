from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

roles = Blueprint('roles', __name__, template_folder='templates', static_folder='static')
htmlfile = 'role.html'

def role_template(htmlfile=None, extra=None, action=None):
    return render_template(htmlfile,
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
