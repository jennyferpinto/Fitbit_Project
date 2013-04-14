from app import app
from flask import Flask, render_template, redirect, request, session

@app.route('/home')
def home():
  return render_template("base.html", users = users)

@app.route('/login')
def login():
  return render_template("home.html")

# include views for after login - patients and therapists

# http://localhost:6543/
# http://localhost:7654/apps/home/jesse/
# http://localhost:7654/comment

# action="/comment"
# 'comment' => '/comment'
# action="{{ 'comment' | route }}"