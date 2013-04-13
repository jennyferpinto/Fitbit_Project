from flask import Flask

app = Flask(__name__)
# app.config.from_object('config') -- if I want to use openID

from app import views
