from app import app
from flask import Flask, render_template, redirect, request, session

@app.route('/home')
def home():
  return render_template("base.html", users = users)

@app.route('/login')
def login():
  return render_template("home.html")

# include views for after login - patients and therapists
