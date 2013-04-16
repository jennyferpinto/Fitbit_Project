from app import app
from flask import Flask, render_template, redirect, request, session
from flask import request, g, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, SignUpForm
import model
from flask.ext.login import LoginManager, current_user
from model import Users, Activity
from flaskext.bcrypt import Bcrypt

# below all needed for Flask-Login to work
login_manager = LoginManager()
login_manager.setup_app(app)
# redirects them to here if they aren't logged in where they are supposed to be
login_manager.login_view = "users.login"

# for bcrypt
bcrypt = Bcrypt(app)
# to use:
# pw_hash = bcrypt.generate_password_hash('hunter2')
# bcrypt.check_password_hash(pw_hash, 'hunter2') # returns True

@app.route('/home')
def home():
  return render_template("base.html")


# allows user_id to be held between page loads
@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))


@app.route("/login", methods = ["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = model.session.query(Users).filter(Users.email == form.email.data).first()
    user_password = user.password
    print "-------------"
    print user_password
    print "-------------"
    unhashed_pwrd = bcrypt.check_password_hash(user_password, form.password.data)
    print "--------------"
    print unhashed_pwrd
    print "--------------"
    if user is not None and unhashed_pwrd == True:
      login_user(user)
      flash("logged in successfully")
      return redirect(url_for("tester"))
    else:
      flash("Incorrect Password")
      return redirect("login")
  return render_template("login.html", title="Sign In", form=form)


@app.route("/test_page")
@login_required
def tester():
  return render_template('page.html')


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("home"))


@app.route('/signup', methods = ["POST","GET"])
def form():
  form = SignUpForm()
  if form.validate_on_submit():
    user = model.session.query(Users).filter(Users.email == form.email.data).first()
    if user != None:
      user_email = user.email
      if user_email == form.email.data:
        flash ("email already exists")
        return redirect(url_for("form"))
    if user == None:
      first_name = form.first_name.data
      last_name = form.last_name.data
      email = form.email.data
      password = form.password.data
      pw_hash = bcrypt.generate_password_hash(password)
      print "---------------------"
      print pw_hash
      print "---------------------"
      # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
      new_user = model.Users(id = None, email=email, password=pw_hash,first_name=first_name, last_name=last_name)
      model.session.add(new_user)
      model.session.commit()
      return redirect("home")
  return render_template("signup.html", title="Sign Up Form", form=form)

# @app.route('/login_done')
# def login_done():
#   return render_template('login_done.html')


@app.route('/patient_home', methods = ["GET", "POST"])
def patient_home():
  activity = fetch_test_activity_row()
  floors = activity.floors
  print floors
  stairs = activity.stairs
  print stairs
  distance = activity.distance
  print distance
  time_object = activity.date # is a datetime object, have to use strptime()
  string_time = str(time_object)
  stripped_time = string_time[:11]
  print stripped_time
  return render_template("patient_home.html")


def fetch_test_activity_row():
  return model.session.query(Activity).get("5")
  # change it to fetch_test_user after I insert a user_id into the activities db table