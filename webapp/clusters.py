from pprint import pprint
from flask import Blueprint, Flask, session, render_template, url_for, request, current_app
import json

clusters = Blueprint('clusters', __name__)
htmlfile = 'clusters.html'

@clusters.route('/', methods=['GET'])
def list_clusters():
    base_url = current_app.base_url + "clusters/"
    pprint(base_url)
    data = json.loads(current_app.build_request(base_url), "GET")
    return current_app.templatify(htmlfile=htmlfile,
                                  action='List',
                                  extra=data)
