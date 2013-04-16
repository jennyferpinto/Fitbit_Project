from flask import Flask, url_for
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.from_object('config')

from app import views



# modifying jinja so that I can include the rickshaw and D3 stuff
# app.jinja_env.globals['static'] = (lambda filename: url_for('static', filename = filename))



