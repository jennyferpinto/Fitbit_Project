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


@app.route('/therapists_patient_homepage', methods = ["POST","GET"])
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
  # weekly_steps_data = util.patients_weekly_steps(patient_id)
  # weekly_floors_data = util.patients_weekly_floors(patient_id)
  # weekly_miles_data = util.patients_weekly_miles(patient_id)
  # days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  # daily_data = util.day_view(days_activity)
  return render_template("therapists_patient_homepage.html", title = "Patient Info", name=name, patient_id=patient_id)



@app.route('/therapists_patients_weekly', methods = ["POST", "GET"])
@login_required
def patients_weekly_graphs():
  patient_id = session.get('patient')
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
  name = patient.first_name
  weekly_steps_data = util.patients_weekly_steps(patient_id)
  weekly_floors_data = util.patients_weekly_floors(patient_id)
  weekly_miles_data = util.patients_weekly_miles(patient_id)

  x_axis = [0,1,2,3,4,5,6]

  steps_list = []
  for element in weekly_steps_data:
    steps_list.append(element.steps)
  x_axis = [0,1,2,3,4,5,6]
  step_tuples = zip(x_axis, steps_list)

  dates_list = []
  for element in weekly_steps_data:
    dates_list.append(element.date.day)
  date_tuples = zip(x_axis, dates_list)

  # days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  # daily_data = util.day_view(days_activity)
  return render_template("therapists_patient_view.html", title = "Patient Weekly Info",
                        weekly_steps_data=weekly_steps_data,
                        weekly_floors_data=weekly_floors_data,
                        weekly_miles_data=weekly_miles_data,
                        name=name,
                        x_axis=x_axis,
                        date_tuples=date_tuples,
                        step_tuples=step_tuples)


@app.route('/therapists_patients_daily', methods=["POST", "GET"])
@login_required
def therapists_patients_daily():
  patient_id = session.get('patient')
  patient = model.session.query(Users).filter(Users.id == patient_id).first()
  name = patient.first_name
  # days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  # daily_data = util.day_view(days_activity)
  daily_data = util.day_view(patient_id)
  steps = daily_data.steps
  floors = daily_data.floors
  distance = daily_data.distance
  time_object = daily_data.date
  string_time = str(daily_data.date)
  stripped_time = string_time[:11]
  days_list = [steps, floors, distance]
  x_list = [0,1,2]
  daily_tuples = zip(x_list, days_list)
  return render_template("therapists_patients_daily.html",
                          title="Patient Daily Info",
                          daily_data=daily_data,
                          name=name,
                          steps=steps,
                          floors=floors,
                          distance=distance,
                          days_list=days_list,
                          daily_tuples=daily_tuples)


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

@app.route('/day_view', methods = ["POST", "GET"])
@login_required
def day_view():
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
  print days_list
  x_list = [0,1,2]
  daily_tuples = zip(x_list, days_list)
  print "+++++++++++++++++++++++++++++++++++++++++++++"
  print daily_tuples
  print "+++++++++++++++++++++++++++++++++++++++++++++"
  # days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id).first()
  # # gets all the floors, steps, distance info to display it as text
  # floors = days_activity.floors
  # steps = days_activity.steps
  # distance = days_activity.distance
  # time_object = days_activity.date
  # string_time = str(time_object)
  # # stripped the time to exclude everything but year, month, day
  # stripped_time = string_time[:11]
  # daily_data = util.day_view(days_activity)
  return render_template("day_view.html", title="Day Overview",
                        floors=floors,
                        steps=steps,
                        distance=distance,
                        stripped_time=stripped_time,
                        name=name,
                        time_object=time_object,
                        days_list=days_list,
                        daily_tuples=daily_tuples)


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

  daily_goals = util.days_goals(current_user_id)
  steps_goal = daily_goals.step_goal
  floors_goal = daily_goals.floors_goal
  distance_goal = daily_goals.distance_goal
  time_goal_set = daily_goals.date
  goal_date = str(time_goal_set)
  stripped_goal_date = goal_date[:10]
  print "____________________________________________________________________"
  print stripped_goal_date
  print "____________________________________________________________________"


  goals_list = [steps_goal, floors_goal, distance_goal]
  daily_goals_tuples = zip(x_list, goals_list)

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
                        daily_activity_tuples=daily_activity_tuples)

@app.route('/weekly_steps', methods = ["GET","POST"])
@login_required
def weekly_steps_chart():
  current_user_id = current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id)
  weekly_steps_data = util.patients_weekly_steps(current_user.id)

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

@app.route('/weekly_floors', methods = ["GET","POST"])
@login_required
def weekly_floors_chart():
  current_user_id = current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id)
  # weekly_steps_data = util.patients_weekly_steps(current_user.id)
  weekly_floors_data = util.patients_weekly_floors(current_user.id)
  # weekly_miles_data = util.patients_weekly_miles(current_user.id)
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

@app.route('/weekly_miles', methods = ["GET","POST"])
@login_required
def weekly_miles_chart():
  current_user_id = current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id)
  # weekly_steps_data = util.patients_weekly_steps(current_user.id)
  # weekly_floors_data = util.patients_weekly_floors(current_user.id)
  weekly_miles_data = util.patients_weekly_miles(current_user.id)
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


