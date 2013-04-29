from app import app
from flask import Flask, render_template, redirect, request, session, g
from flask import request, g, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, SignUpForm, GoalsForm
import model
from flask.ext.login import LoginManager, current_user
from model import Users, Activity, Goal
from flaskext.bcrypt import Bcrypt
import util
import fitbit
from sqlalchemy import desc
import datetime
import json

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
  # dont allow user to re-login after they've done so
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
    # current_user_id = current_user.id
    if user is not None and unhashed_pwrd == True:
      login_user(user)
      user.last_login = datetime.datetime.utcnow()
      user.number_logins += 1
      model.session.commit()
      flash("logged in successfully")
      if current_user.role == "patient":
        return redirect(url_for("patient_home"))
      else:
        return redirect(url_for("therapist_home"))
    # add something else in for when user is already logged in
    else:
      flash("Incorrect Password")
      return redirect(url_for("login"))
  return render_template("login.html", title="Sign In", form=form)

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
  #insert role into the sign up form, to differentiate btwn patients/therapists
  form = SignUpForm()
  if form.validate_on_submit():
    # queries for the email submitted in the signup form
    user = model.session.query(Users).filter(Users.email == form.email.data).first()
    if user is not None:
      # checking to see if the email is already in the database
      user_email = user.email
      if user_email == form.email.data:
        flash ("email already exists")
        return redirect(url_for("form"))
    # if it is actually a new user then it pulls wtf forms data and assigns it to variables
    if user == None:
      first_name = form.first_name.data
      last_name = form.last_name.data
      role = form.role.data
      if role == 'therapist':
        therapist = None
      email = form.email.data
      password = form.password.data
      pw_hash = bcrypt.generate_password_hash(password)
      number_logins = 0
      therapist_name = form.therapist_name.data
      if role == 'patient':
        therapist_query = model.session.query(Users).filter(Users.first_name == therapist_name).first()
        therapist = therapist_query.id
        if therapist_query is None:
          flash("therapist not registered")
      new_user = model.Users(id = None,
                            email=email,
                            password=pw_hash,
                            first_name=first_name,
                            last_name=last_name,
                            role=role,
                            number_logins=number_logins,
                            therapist=therapist)
      model.session.add(new_user)
      model.session.commit()
      flash("Account Creation successful, Login to your account")
      return redirect(url_for("home"))
  return render_template("signup.html", title="Sign Up Form", form=form)


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


@app.route('/therapist_home', methods = ["POST", "GET"])
@login_required
def therapist_home():
  name = current_user.first_name
  therapist_id = current_user.id
  return render_template("therapist_home.html", title = "Welcome",
                        name = name)


@app.route('/patients_list', methods = ["POST", "GET"])
@login_required
def patients_list():
  name = current_user.first_name
  therapist_id = current_user.id
  all_patients = model.session.query(Users).filter(Users.therapist == therapist_id).all()
  patients_list = []
  for i in all_patients:
    patients_list.append(i)
  return render_template("patients_list.html", title = "Patients",
                        name = name,
                        patients_list = patients_list)


@app.route('/therapists_patient_view', methods = ["POST","GET"])
@login_required
def therapists_patient_view():
  therapist_id = current_user.id
  patient_info = model.session.query(Users).filter(Users.therapist == therapist_id).all()
  # query for patient's id
  patient_id = request.args.get('patient_id', 0)
  session['patient'] = patient_id
  # activity = patient_info[0].activities
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
  name = patient.first_name
  all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).limit(7)
  weekly_steps_data = util.patients_weekly_steps(all_user_activity)
  weekly_floors_data = util.patients_weekly_floors(all_user_activity)
  weekly_miles_data = util.patients_weekly_miles(all_user_activity)
  days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  daily_data = util.day_view(days_activity)
  return render_template("therapists_patient_view.html", title = "Patient Info",
                        weekly_steps_data=weekly_steps_data,
                        weekly_floors_data=weekly_floors_data,
                        weekly_miles_data=weekly_miles_data,
                        daily_data=daily_data,
                        name=name,
                        patient_id=patient_id)


@app.route('/set_goals', methods = ["POST", "GET"])
@login_required
def set_goals():
  patient_id = session.get('patient')
  # patient_id = request.args.get('patient_id', 0)
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
  print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  print patient
  print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  name = patient.first_name
  form = GoalsForm()
  if form.validate_on_submit():
    steps = form.steps.data
    floors = form.floors.data
    distance = form.distance.data
    date = form.date.data
    new_goals = model.Goal(user_id = patient_id, step_goal = steps, floors_goal = floors, distance_goal = distance, date=date)
    model.session.add(new_goals)
    model.session.commit()
    flash("goals submitted")
  return render_template("set_goals.html", title = "Set Goals", name = name, form=form, patient_id=patient_id)


@app.route('/patient_home', methods = ["POST", "GET"])
@login_required
def patient_home():
  name = current_user.first_name
  return render_template("patient_home.html", title = "Patient",
                        name = name)


@app.route('/day_view', methods = ["POST", "GET"])
@login_required
def day_view():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id).first()
  # gets all the floors, steps, distance info to display it as text
  floors = days_activity.floors
  steps = days_activity.steps
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(time_object)
  # stripped the time to exclude everything but year, month, day
  stripped_time = string_time[:11]
  daily_data = util.day_view(days_activity)
  return render_template("day_view.html", title = "Day Overview",
                        floors = floors,
                        steps = steps,
                        distance = distance,
                        stripped_time = stripped_time,
                        daily_data = daily_data,
                        name = name)


# @app.route('/days_goals', methods = ["POST", "GET"])
# @login_required
# def days_goals():
#   current_user_id = current_user.id
#   days_goals = model.session.query(Goal).order_by(Goal.date.desc()).filter(Goal.user_id == current_user_id).first()
#   days_activity = model.session.query(Activity).order_by(Activity.date.desc().filter(Activity.user_id == current_user_id).first()
#   floors = days_activity.floors
#   steps = days_activity.steps
#   distance = days_activity.distance
#   time_object = days_activity.date
#   string_time = str(time_object)
#   floors_goal = days_goals.floors_goal
#   steps_goal = days_goals.step_goal
#   distance_goal = days_goals.distance_goal
#   time_object = days_goals.date
#   string_time = str(time_object)
#   stripped_time = string_time[:11]

#   return render_template("days_goals.html", title = "Days Goals",
#                         floors_goal=floors_goal,
#                         steps_goal=steps_goal,
#                         distance_goal=distance_goal,
#                         stripped_time=stripped_time,
#                         floors=floors,
#                         steps=steps,
#                         distance=distance
#                         )


# def steps_by_day(activity):
#   steps = util.weekly_steps(activity)
#   # steps = [5] * 7
#   # dates = util.dates_for_week(activity)
#   today = datetime.datetime.today()
#   days = []
#   for i in range(7):
#     days.append( today - datetime.timedelta(days=i))
#   dates = [int(d.strftime("%s")) for d in days]
#   return zip(dates, steps)

@app.route('/weekly_data', methods = ["GET"])
@login_required
def weekly_data_charts():
  current_user_id = current_user.id
  all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id)

  weekly_steps_data = util.patients_weekly_steps(current_user.id)
  weekly_floors_data = util.patients_weekly_floors(all_user_activity)
  weekly_miles_data = util.patients_weekly_miles(all_user_activity)
  return render_template("steps_weekly.html",
                        weekly_steps_data=weekly_steps_data,
                        weekly_floors_data=weekly_floors_data,
                        weekly_miles_data=weekly_miles_data)


