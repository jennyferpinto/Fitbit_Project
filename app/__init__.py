from flask import Flask, url_for

app = Flask(__name__)
# app.config.from_object('config') -- if I want to use openID

# modifying jinja so that I can include the rickshaw and D3 stuff
app.jinja_env.globals['static'] = (lambda filename: url_for('static', filename=filename))

from app import views