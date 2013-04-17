from app import app
from flask import Flask, render_template, redirect, request, session
from flask import request, g, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, SignUpForm
import model
from flask.ext.login import LoginManager, current_user
from model import Users, Activity
from flaskext.bcrypt import Bcrypt
import util
import fitbit

# below all needed for Flask-Login to work
login_manager = LoginManager()
login_manager.setup_app(app)

# redirects them to here if they aren't logged in, when they are supposed to be for that page
# can customize the message
# right now what it does is: redirects them to the login page and flashes "Please log in to access this page."
login_manager.login_view = "login"

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
    # print "-------------"
    # print user_password
    # print "-------------"
    unhashed_pwrd = bcrypt.check_password_hash(user_password, form.password.data)
    # print "--------------"
    # print unhashed_pwrd
    # print "--------------"
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
  flash("You are now logged out")
  # logged_in_user_id = current_user.id
  # print "***********************************************************"
  # print logged_in_user_id
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
      # print "---------------------"
      # print pw_hash
      # print "---------------------"
      new_user = model.Users(id = None,
                            email=email,
                            password=pw_hash,
                            first_name=first_name,
                            last_name=last_name)
      model.session.add(new_user)
      model.session.commit()
      return redirect("home")
  return render_template("signup.html", title="Sign Up Form", form=form)

# @app.route('/login_done')
# def login_done():
#   return render_template('login_done.html')

@app.route('/sync_fitbit', methods = ["GET"])
@login_required
def fitbit_sync():
  # hard coded me as user so that I can retrieve my data
  user = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90',
                       'e2b38ed6dad443e8bad8efbe3e0e3da5',
                       user_key="5fec83e8ad9ea52dd63b47a42b87b852",
                       user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")
  # if user.activities(left blank) then it will get the most recent activity for that user
  user_info = user.activities()
  # uses the current_user function from flask-login to get the id of the user who is logged in
  user_id = current_user.id
  # modified the insert_activities function from util.py to take two arguments
  new_activity = util.insert_activities(user_info, user_id)
  model.session.add(new_activity)
  model.session.commit()
  flash("Fitbit is synced!")
  return redirect(url_for("patient_home"))


@app.route('/patient_home', methods = ["POST", "GET"])
@login_required
def patient_home():
  activity = fetch_test_activity_row()
  print activity
  floors = activity.floors
  print floors
  steps = activity.steps
  print steps
  distance = activity.distance
  print distance
  time_object = activity.date
  string_time = str(time_object)
  # stripped the time to exclude everything but year, month, day
  stripped_time = string_time[:11]
  print stripped_time
  return render_template("patient_home.html", title = "Patient",
                          steps=steps,
                          floors=floors,
                          distance=distance,
                          stripped_time=stripped_time)

def fetch_test_activity_row():
  return model.session.query(Activity).get("5")
  # return session.query(Activity).order_by(Activity.id.desc()).first()
# change it to fetch_test_user after I insert a user_id into the activities db table