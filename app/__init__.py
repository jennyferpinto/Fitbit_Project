from flask import Flask, url_for
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.from_object('config')

from app import views
import model

model.initialize()