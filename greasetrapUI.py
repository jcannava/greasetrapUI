import os
import sys
import logging 
import httplib2
import json

abspath = os.path.dirname(__file__)
sys.path.append(abspath)

from pprint import pprint
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

def build_request(url=None, verb=None, data=None):
    headers = {"Content-Type": "application/json"}
    conn = httplib2.Http()
    resp, content = conn.request(url, verb, data, headers)
    return content

def templatify(htmlfile=None, action=None, extra=None):
    if htmlfile == 'cluster.html':
        return render_template(htmlfile,
                           clusters=url_for('clusters'),
                           nodes=url_for('nodes'),
                           roles=url_for('roles'),
                           css=url_for('static', filename='site.css'),
                           action=action,
                           data=extra)
    elif htmlfile == 'node.html':
        return render_template(htmlfile,
                           clusters=url_for('clusters'),
                           nodes=url_for('nodes'),
                           roles=url_for('roles'),
                           css=url_for('static', filename='site.css'),
                           action=action,
                           data=extra)
    elif htmlfile == 'role.html':
        return render_template(htmlfile,
                           clusters=url_for('clusters'),
                           nodes=url_for('nodes'),
                           roles=url_for('roles'),
                           css=url_for('static', filename='site.css'),
                           action=action,
                           data=extra)
    else:
        return render_template('index.html', 
                           clusters=url_for('clusters'), 
                           nodes=url_for('nodes'), 
                           roles=url_for('roles'),
                           css=url_for('static', filename='site.css'))

@app.route('/')
def greaseTrap():
    return render_template('index.html', 
                           clusters=url_for('clusters'), 
                           nodes=url_for('nodes'), 
                           roles=url_for('roles'),
                           css=url_for('static', filename='site.css'))

@app.route('/clusters')
@app.route('/clusters/<verb>', methods=['GET','POST']) 
@app.route('/clusters/<verb>/<id>', methods=['GET', 'POST'])
def clusters(verb=None, id=None):
    url = "http://%s:%d/clusters/" % (roush_address, roush_port)
    if verb == 'list' or verb == None:
        return templatify(htmlfile='cluster.html', 
                          action='List', 
                          extra=json.loads(build_request(url, "GET")))

    elif verb == 'create' and request.method == 'GET':
        return templatify(htmlfile='cluster.html', action='Create')

    elif verb == 'create' and request.method == 'POST':
        jdata = json.dumps({"name": request.form['cluster_name'], 
                            "description": request.form['cluster_descr']}).encode('utf-8')
        build_request(url, "POST", jdata)
        return templatify(htmlfile='cluster.html', action='List', extra=json.loads(build_request(url,"GET")))

    elif verb == 'update' and id != None and request.method == "GET":
        update_url = url + id
        return templatify(htmlfile='cluster.html', action='Update', extra=json.loads(build_request(update_url, "GET")))
    
    elif verb == 'update' and id != None and request.method == "POST":
        update_url = url + id
        jdata = json.dumps({"name": request.form['cluster_name'],
                           "description": request.form['cluster_descr']}).encode('utf-8')
        build_request(update_url, "PUT", jdata)
        return templatify(htmlfile='cluster.html', 
                          action='List', 
                          extra=json.loads(build_request(url, "GET")))

    elif verb == 'delete':
        delete_url = url + id
        build_request(delete_url, "DELETE")
        return templatify(htmlfile='cluster.html', 
                          action='List', 
                          extra=json.loads(build_request(url, "GET")))


@app.route('/nodes')
@app.route('/nodes/<verb>', methods=['GET', 'POST'])
@app.route('/nodes/<verb>/<id>', methods=['GET', 'POST'])
def nodes(verb=None, id=None):
    url = "http://%s:%d/nodes/" % (roush_address, roush_port)
    if verb == 'list' or verb == None:
        return templatify(htmlfile='node.html',
                          action='List',
                          extra=json.loads(build_request(url, "GET")))
    ### TODO: Create, Update, Delete mechanisms.

@app.route('/roles')
@app.route('/roles/<verb>', methods=['GET', 'POST'])
@app.route('/roles/<verb>/<id>', methods=['GET', 'POST'])
def roles(verb=None, id=None):
    url = "http://%s:%d/roles/" % (roush_address, roush_port)
    if verb == 'list' or verb == None:
        return templatify(htmlfile='role.html',
                          action='List',
                          extra=json.loads(build_request(url, "GET")))
   
    elif verb == 'create' and request.method == 'GET':
        return templatify(htmlfile='role.html', action='Create')

    elif verb == 'create' and request.method == 'POST':
        jdata = json.dumps({"name": request.form['role_name'],
                            "description": request.form['role_descr']}).encode('utf-8')
        build_request(url, "POST", jdata)
        return templatify(htmlfile='role.html', action='List', extra=json.loads(build_request(url,"GET")))

    elif verb == 'update' and id != None and request.method == "GET":
        update_url = url + id
        return templatify(htmlfile='role.html', action='Update', extra=json.loads(build_request(update_url, "GET")))
    
    elif verb == 'update' and id != None and request.method == "POST":
        update_url = url + id
        jdata = json.dumps({"name": request.form['role_name'],
                           "description": request.form['role_descr']}).encode('utf-8')
        build_request(update_url, "PUT", jdata)
        return templatify(htmlfile='role.html', 
                          action='List', 
                          extra=json.loads(build_request(url, "GET")))

    elif verb == 'delete':
        delete_url = url + id
        build_request(delete_url, "DELETE")
        return templatify(htmlfile='role.html', 
                          action='List', 
                          extra=json.loads(build_request(url, "GET")))

if __name__ == '__main__':
    debug = True
    bind_address = '0.0.0.0'
    bind_port = 8081
    roush_address ='127.0.0.1'
    roush_port = 8080

    # set up logging
    LOG = logging.getLogger()
    LOG.addHandler(logging.FileHandler("/dev/stderr"))

    LOG.debug("Starting greasetrapUI on %s:%d" % (bind_address, bind_port))
    app.run(host=bind_address, port=bind_port, debug=debug)   
