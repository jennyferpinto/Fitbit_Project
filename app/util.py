import model
from datetime import datetime, date, timedelta
import json
from model import Users, Activity, Goal

def insert_activities(dictionary, user_id):
  # inserts user's synced activity data into the database
  all_miles = dictionary['summary']['distances'][0]
  total_miles = all_miles['distance']
  total_cals = dictionary['summary']['caloriesOut']
  total_steps = dictionary['summary']['steps']
  total_floors = dictionary['summary']['floors']
  s_mins = dictionary['summary']['sedentaryMinutes']
  la_mins = dictionary['summary']['lightlyActiveMinutes']
  fa_mins = dictionary['summary']['fairlyActiveMinutes']
  va_mins = dictionary['summary']['veryActiveMinutes']
  bmr = dictionary['summary']['caloriesBMR']
  activity_cals = dictionary['summary']['activityCalories']
  date = datetime.utcnow()
  # today = datetime.today()
  # days = []
  # for i in range(8):
  #   days.append(today - timedelta(days=i))
  # date = days[0]
  everything_updated = model.Activity(id=None, user_id=user_id,
                                      floors=total_floors,
                                     steps=total_steps,
                                      sedentary_min=s_mins,
                                      lightly_active_min=la_mins,
                                      fairly_active_min=fa_mins,
                                      very_active_min=va_mins,
                                      total_cal=total_cals,
                                      bmr=bmr,
                                      activity_cals=activity_cals,
                                      distance=total_miles,
                                      date=date)
  return everything_updated


def patients_weekly_steps(patient_id):
  start = date.today() - timedelta(days=8)
  print date.today()
  query = model.session.query(Activity).\
            order_by(Activity.date.asc()).\
            filter(Activity.user_id == patient_id).\
            filter(Activity.date > start).\
            filter(Activity.date <= date.today()).\
            limit(7)
  return query.all()


def patients_weekly_floors(patient_id):
  start = date.today() - timedelta(days=8)

  query = model.session.query(Activity).\
            order_by(Activity.date.asc()).\
            filter(Activity.user_id == patient_id).\
            filter(Activity.date > start).\
            filter(Activity.date <= date.today()).\
            limit(7)
  return query.all()


def patients_weekly_miles(patient_id):
  start = date.today() - timedelta(days=8)

  query = model.session.query(Activity).\
            order_by(Activity.date.asc()).\
            filter(Activity.user_id == patient_id).\
            filter(Activity.date > start).\
            filter(Activity.date <= date.today()).\
            limit(7)
  return query.all()


def day_view(patient_id):
  patients_day = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  return patients_day


def month_view(patient_id):
  pass

def yesterday_info(patient_id):
  start = date.today() - timedelta(days=1)
  query = model.session.query(Activity).\
            order_by(Activity.date.desc()).\
            filter(Activity.user_id == patient_id).\
            filter(Activity.date >= start).\
            filter(Activity.date < date.today()).\
            first()
  return query

def days_goals(patient_id):
  days_goals = model.session.query(Goal).order_by(Goal.id.desc()).filter(Goal.user_id == patient_id).first()
  return days_goals

def days_activity(patient_id):
  days_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == patient_id).first()
  return days_activity