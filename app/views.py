from app import app
from flask import Flask, render_template, redirect, request, session, g
from flask import request, g, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, SignUpTherapistForm, GoalsForm, SignUpPatientForm
import model
from flask.ext.login import LoginManager, current_user
from model import Users, Activity, Goal
from flaskext.bcrypt import Bcrypt
import util
import fitbit
from sqlalchemy import desc
import datetime
import json
import fitbit_auth

# below all needed for Flask-Login to work
login_manager = LoginManager()
login_manager.setup_app(app)


# redirects them to here if they aren't logged in, when they are supposed to be for that page
# can customize the message
# right now what it does is: redirects them to the login page and flashes "Please log in to access this page."
login_manager.login_view = "login"

# for bcrypt
bcrypt = Bcrypt(app)


@app.route('/home')
def home():
  return render_template("base.html")


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
    unhashed_pwrd = bcrypt.check_password_hash(user_password, form.password.data)
    if user is not None and unhashed_pwrd == True:
      login_user(user)
      user.last_login = datetime.datetime.utcnow()
      user.number_logins += 1
      model.session.commit()
      # flash("logged in successfully")
      if current_user.role == "patient":
        return redirect(url_for("patient_home"))
      else:
        return redirect(url_for("therapist_home"))
    else:
      flash("Incorrect Password")
      return redirect(url_for("login"))
  return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You are now logged out")
  return redirect(url_for("home"))


@app.route('/signup', methods=["POST","GET"])
def base_form():
  return render_template("base_form.html", title="Sign Up!")


@app.route('/signup_therapist', methods = ["POST","GET"])
def therapist_form():
  #insert role into the sign up form, to differentiate btwn patients/therapists
  form = SignUpTherapistForm()
  if form.validate_on_submit():
    # queries for the email submitted in the signup form
    user = model.session.query(Users).filter(Users.email == form.email.data).first()
    if user is not None:
      # checking to see if the email is already in the database
      user_email = user.email
      if user_email == form.email.data:
        flash ("email already exists")
        return redirect(url_for("therapist_form"))
    # if it is actually a new user then it pulls wtf forms data and assigns it to variables
    if user == None:
      first_name = form.first_name.data
      last_name = form.last_name.data
      role = form.role.data
      email = form.email.data
      password = form.password.data
      pw_hash = bcrypt.generate_password_hash(password)
      number_logins = 0
      new_user = model.Users(id = None,
                            email=email,
                            password=pw_hash,
                            first_name=first_name,
                            last_name=last_name,
                            role=role,
                            number_logins=number_logins)
      model.session.add(new_user)
      model.session.commit()
      flash("Account Creation successful, Login to your account")
      return redirect(url_for("home"))
  return render_template("therapist_form.html", title="Sign Up Form", form=form)


@app.route('/signup_patient', methods = ["POST","GET"])
def patient_form():
  #insert role into the sign up form, to differentiate btwn patients/therapists
  form = SignUpPatientForm()
  if form.validate_on_submit():
    # queries for the email submitted in the signup form
    user = model.session.query(Users).filter(Users.email == form.email.data).first()
    if user is not None:
      # checking to see if the email is already in the database
      user_email = user.email
      if user_email == form.email.data:
        flash ("email already exists")
        return redirect(url_for("patient_form"))
    # if it is actually a new user then it pulls wtf forms data and assigns it to variables
    if user == None:
      first_name = form.first_name.data
      last_name = form.last_name.data
      role = form.role.data
      email = form.email.data
      password = form.password.data
      pw_hash = bcrypt.generate_password_hash(password)
      number_logins = 0
      therapist = form.therapist.data.id
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
  return render_template("patient_form.html", title="Sign Up Form", form=form)


@app.route('/patient_account', methods = ["POST", "GET"])
@login_required
def patient_account():
  user = model.session.query(Users).filter(Users.id == current_user.id).one()
  name = user.first_name
  return render_template("patient_account.html",
                          title="User Account",
                          name=name)


@app.route('/authorize_fitbit', methods = ["POST","GET"])
@login_required
def fitbit_access():
  auth_url, access_token = fitbit_auth.get_request_token()
  user = model.session.query(Users).filter(Users.id == current_user.id).one()
  user.user_secret = access_token.secret
  user.user_key = access_token.key
  model.session.add(user)
  model.session.commit()
  return redirect(auth_url)


@app.route('/handshake', methods = ["POST", "GET"])
@login_required
def oauth_complete():
  user = model.session.query(Users).filter(Users.id == current_user.id).one()
  user.verifier = request.args.get('oauth_verifier')
  token = fitbit_auth.get_access_token(user.verifier, user.user_key, user.user_secret)
  user.user_secret = token.secret
  user.user_key = token.key
  model.session.add(user)
  model.session.commit()
  flash("Congrats! You've authorized your Fitbit!")
  return redirect(url_for("home"))


@app.route('/sync_fitbit', methods = ["GET"])
@login_required
def fitbit_sync():
  user_account = model.session.query(Users).filter(Users.id == current_user.id).one()
  user_secret = user_account.user_secret
  user_key = user_account.user_key
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
  return render_template("patients_list.html", title="Patients",
                        name=name,
                        patients_list=patients_list)


@app.route('/therapists_patient_homepage', methods = ["POST","GET"])
@login_required
def therapists_patient_view():
  therapist_id = current_user.id
  patient_info = model.session.query(Users).filter(Users.therapist == therapist_id).all()
  patient_id = request.args.get('patient_id', 0)
  session['patient'] = patient_id
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
  name = patient.first_name
  return render_template("therapists_patient_homepage.html", title="Patient Info", name=name, patient_id=patient_id)


@app.route('/set_goals', methods = ["POST", "GET"])
@login_required
def set_goals():
  patient_id = session.get('patient')
  # patient_id = request.args.get('patient_id', 0)
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
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


@app.route('/therapist_patients_goals', methods = ["POST", "GET"])
@login_required
def therapist_patients_goals():
  patient_id = session.get('patient')
  # current_user_id = current_user.id
  # name = current_user.first_name
  days_activity = util.days_activity(patient_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]
  days_list = [steps, floors, distance]
  x_list = [0,1,2]
  daily_activity_tuples = zip(x_list, days_list)
  bars = ['Steps', 'Floors', 'Miles']
  format_tuples = zip(x_list,bars)
  daily_goals = util.days_goals(patient_id)
  if daily_goals is not None:
    steps_goal = daily_goals.step_goal
    floors_goal = daily_goals.floors_goal
    distance_goal = daily_goals.distance_goal
    time_goal_set = daily_goals.date
    goal_date = str(time_goal_set)
    stripped_goal_date = goal_date[:10]
    goals_list = [steps_goal, floors_goal, distance_goal]
    daily_goals_tuples = zip(x_list, goals_list)
  else:
    steps_goal = 0
    floors_goal = 0
    distance_goal = 0
    stripped_goal_date = "No Goals Set For Today"
    flash("No goals set")
  return render_template("therapist_patients_goals.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        floors_goal=floors_goal,
                        steps_goal=steps_goal,
                        distance_goal=distance_goal,
                        time_object=time_object,
                        stripped_goal_data=stripped_goal_date,
                        daily_goals_tuples=daily_goals_tuples,
                        daily_activity_tuples=daily_activity_tuples,
                        format_tuples=format_tuples)


# @app.route('/monthly_view', methods=["POST", "GET"])
# @login_required
# def month_graph():
#   current_user = current_user.id
#   month_info = util.monthly_activity(current_user)
#   steps = month_info.steps
#   points = len(steps)
#   print points
#   return render_template("monthly_view.html",
#                           title="Monthly Activity"
#                           steps_tuple=steps_tuple)


@app.route('/days_goals_graph', methods = ["POST", "GET"])
@login_required
def days_goals_graph():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = util.days_activity(current_user_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]
  days_list = [steps, floors, distance]
  x_list = [0,1,2]
  daily_activity_tuples = zip(x_list, days_list)
  bars = ['Steps', 'Floors', 'Miles']
  format_tuples = zip(x_list,bars)
  daily_goals = util.days_goals(current_user_id)
  if daily_goals is not None:
    steps_goal = daily_goals.step_goal
    floors_goal = daily_goals.floors_goal
    distance_goal = daily_goals.distance_goal
    time_goal_set = daily_goals.date
    goal_date = str(time_goal_set)
    stripped_goal_date = goal_date[:10]
    goals_list = [steps_goal, floors_goal, distance_goal]
    daily_goals_tuples = zip(x_list, goals_list)
  else:
    steps_goal = 0
    floors_goal = 0
    distance_goal = 0
    stripped_goal_date = "No Goals Set For Today"
    flash("No goals set")
  return render_template("days_goals_graph.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        floors_goal=floors_goal,
                        steps_goal=steps_goal,
                        distance_goal=distance_goal,
                        time_object=time_object,
                        stripped_goal_data=stripped_goal_date,
                        daily_goals_tuples=daily_goals_tuples,
                        daily_activity_tuples=daily_activity_tuples,
                        format_tuples=format_tuples)


@app.route('/days_goals', methods = ["POST", "GET"])
@login_required
def days_goals():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = util.days_activity(current_user_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]
  days_list = [steps, floors, distance]
  x_list = [0,1,2]
  daily_activity_tuples = zip(x_list, days_list)
  bars = ['Steps', 'Floors', 'Miles']
  format_tuples = zip(x_list,bars)
  daily_goals = util.days_goals(current_user_id)
  if daily_goals is not None:
    steps_goal = daily_goals.step_goal
    floors_goal = daily_goals.floors_goal
    distance_goal = daily_goals.distance_goal
    time_goal_set = daily_goals.date
    goal_date = str(time_goal_set)
    stripped_goal_date = goal_date[:10]
    goals_list = [steps_goal, floors_goal, distance_goal]
    daily_goals_tuples = zip(x_list, goals_list)
  else:
    steps_goal = 0
    floors_goal = 0
    distance_goal = 0
    stripped_goal_date = "No Goals Set For Today"
    flash("No goals set")
  return render_template("days_goals.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        floors_goal=floors_goal,
                        steps_goal=steps_goal,
                        distance_goal=distance_goal,
                        time_object=time_object,
                        stripped_goal_data=stripped_goal_date,
                        daily_goals_tuples=daily_goals_tuples,
                        daily_activity_tuples=daily_activity_tuples,
                        format_tuples=format_tuples)


@app.route('/daily_steps_activity', methods = ["GET", "POST"])
@login_required
def days_steps_activity():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = util.days_activity(current_user_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]

  x_list  =[0,1]
  yesterdays_info = util.yesterday_info(current_user_id)
  if yesterdays_info is None:
    flash("No data from yesterday")
    yesterdays_steps = 0
    steps_list = [yesterdays_info, steps]
    steps_tuple = zip(x_list, steps_list)
  else:
    yesterdays_steps = yesterdays_info.steps
    steps_list = [yesterdays_steps, steps]
    steps_tuple = zip(x_list, steps_list)

  bars = ["Yesterday", "Today"]
  format_tuples = zip(x_list,bars)

  return render_template("days_steps_activity.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        steps_tuple=steps_tuple,
                        format_tuples=format_tuples)


@app.route('/daily_distance_activity', methods = ["GET", "POST"])
@login_required
def days_distance_activity():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = util.days_activity(current_user_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]

  x_list  =[0,1]
  yesterdays_info = util.yesterday_info(current_user_id)
  if yesterdays_info is None:
    flash("No data from yesterday")
    yesterdays_distance = 0
    distance_list = [yesterdays_info, steps]
    distance_tuple = zip(x_list, steps_list)
  else:
    yesterdays_distance = yesterdays_info.distance
    distance_list = [yesterdays_distance, distance]
    distance_tuple = zip(x_list, distance_list)

  bars = ["Yesterday", "Today"]
  format_tuples = zip(x_list,bars)
  return render_template("days_distance_activity.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        format_tuples=format_tuples,
                        distance_tuple=distance_tuple)


@app.route('/daily_floors_activity', methods = ["GET", "POST"])
@login_required
def days_floors_activity():
  current_user_id = current_user.id
  name = current_user.first_name
  days_activity = util.days_activity(current_user_id)
  steps = days_activity.steps
  floors = days_activity.floors
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(days_activity.date)
  stripped_time = string_time[:11]

  x_list  =[0,1]
  yesterdays_info = util.yesterday_info(current_user_id)
  if yesterdays_info is None:
    flash("No data from yesterday")
    yesterdays_floors = 0
    floors_list = [yesterdays_info, steps]
    floors_tuple = zip(x_list, steps_list)
  else:
    yesterdays_floors = yesterdays_info.floors
    floors_list = [yesterdays_floors, floors]
    floors_tuple = zip(x_list, floors_list)

  bars = ["Yesterday", "Today"]
  format_tuples = zip(x_list,bars)
  return render_template("days_floors_activity.html",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        format_tuples=format_tuples,
                        floors_tuple=floors_tuple)

@app.route('/therapist_weekly_steps', methods = ["GET", "POST"])
@login_required
def therapist_weekly_steps():
  patient_id = session.get('patient')
  weekly_steps_data = util.patients_weekly_steps(patient_id)
  steps_list = []
  for element in weekly_steps_data:
    steps_list.append(element.steps)
  x_axis = [0,1,2,3,4,5,6]
  step_tuples = zip(x_axis, steps_list)
  dates_list = []
  for element in weekly_steps_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  return render_template("therapist_weekly_steps.html",
                        title="Steps",
                        weekly_steps_data=weekly_steps_data,
                        step_tuples=step_tuples,
                        date_tuples=date_tuples)


@app.route('/weekly_steps', methods = ["GET","POST"])
@login_required
def weekly_steps_chart():
  current_user_id = current_user.id
  weekly_steps_data = util.patients_weekly_steps(current_user_id)
  steps_list = []
  for element in weekly_steps_data:
    steps_list.append(element.steps)
  x_axis = [0,1,2,3,4,5,6]
  step_tuples = zip(x_axis, steps_list)
  dates_list = []
  for element in weekly_steps_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  # weekly_floors_data = util.patients_weekly_floors(current_user.id)
  # weekly_miles_data = util.patients_weekly_miles(current_user.id)
  return render_template("steps_weekly.html",
                        title="Steps",
                        weekly_steps_data=weekly_steps_data,
                        step_tuples=step_tuples,
                        date_tuples=date_tuples)


@app.route('/therapist_weekly_floors', methods = ["GET", "POST"])
@login_required
def therapist_weekly_floors():
  patient_id = session.get('patient')
  weekly_floors_data = util.patients_weekly_floors(patient_id)
  floors_list = []
  for element in weekly_floors_data:
    floors_list.append(element.floors)
  x_axis = [0,1,2,3,4,5,6]
  floor_tuples = zip(x_axis, floors_list)
  dates_list = []
  for element in weekly_floors_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  return render_template("therapist_weekly_floors.html",
                        title="Floors",
                        weekly_floors_data=weekly_floors_data,
                        floor_tuples=floor_tuples,
                        date_tuples=date_tuples)


@app.route('/weekly_floors', methods = ["GET","POST"])
@login_required
def weekly_floors_chart():
  current_user_id = current_user.id
  weekly_floors_data = util.patients_weekly_floors(current_user_id)
  floors_list = []
  for element in weekly_floors_data:
    floors_list.append(element.floors)
  x_axis = [0,1,2,3,4,5,6]
  floor_tuples = zip(x_axis, floors_list)
  dates_list = []
  for element in weekly_floors_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  return render_template("floors_weekly.html",
                        title="Floors",
                        weekly_floors_data=weekly_floors_data,
                        floor_tuples=floor_tuples,
                        date_tuples=date_tuples)


@app.route('/therapist_weekly_miles', methods = ["GET","POST"])
@login_required
def therapist_weekly_miles():
  patient_id = session.get('patient')
  weekly_miles_data = util.patients_weekly_miles(patient_id)
  miles_list = []
  for element in weekly_miles_data:
    miles_list.append(element.distance)
  x_axis = [0,1,2,3,4,5,6]
  mile_tuples = zip(x_axis, miles_list)
  dates_list = []
  for element in weekly_miles_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  return render_template("therapist_weekly_miles.html",
                        title="Miles",
                        weekly_miles_data=weekly_miles_data,
                        mile_tuples=mile_tuples,
                        date_tuples=date_tuples)


@app.route('/weekly_miles', methods = ["GET","POST"])
@login_required
def weekly_miles_chart():
  current_user_id = current_user.id
  weekly_miles_data = util.patients_weekly_miles(current_user_id)
  miles_list = []
  for element in weekly_miles_data:
    miles_list.append(element.distance)
  x_axis = [0,1,2,3,4,5,6]
  mile_tuples = zip(x_axis, miles_list)
  dates_list = []
  for element in weekly_miles_data:
    dates_list.append(element.date.strftime('%m'+'.'+'%d'))
  date_tuples = zip(x_axis, dates_list)
  return render_template("miles_weekly.html",
                        title="Miles",
                        weekly_miles_data=weekly_miles_data,
                        mile_tuples=mile_tuples,
                        date_tuples=date_tuples)