import model
import datetime
import fitbit

# nested_dict = the data pulled from c = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90', 'e2b38ed6dad443e8bad8efbe3e0e3da5', user_key="5fec83e8ad9ea52dd63b47a42b87b852", user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")
# user_info = nested_dict

user_info = {u'activities': [], u'goals': {u'floors': 10, u'caloriesOut': 2756, u'activeScore': 1000, u'steps': 10000, u'distance': 8.05}, u'summary': {u'distances': [{u'distance': 5.7, u'activity': u'total'}, {u'distance': 5.7, u'activity': u'tracker'}, {u'distance': 0, u'activity': u'loggedActivities'}, {u'distance': 3.14, u'activity': u'veryActive'}, {u'distance': 2.29, u'activity': u'moderatelyActive'}, {u'distance': 0.27, u'activity': u'lightlyActive'}, {u'distance': 0, u'activity': u'sedentaryActive'}], u'elevation': 103.63, u'sedentaryMinutes': 1020, u'lightlyActiveMinutes': 70, u'caloriesOut': 1633, u'caloriesBMR': 1118, u'marginalCalories': 477, u'fairlyActiveMinutes': 51, u'veryActiveMinutes': 43, u'activityCalories': 670, u'steps': 8286, u'floors': 34, u'activeScore': 553}}


def insert_activities(dictionary):
  pass
  # put all the functions in here

def load_miles(dictionary):
  distance_miles = dictionary['summary']['distances'][0]
  miles = distance_miles['distance']
  # print miles
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add(miles_updated)
  model.session.commit()


def load_calories(dictionary):
  total_cals = user_info['summary']['caloriesOut']
  print total_cals
  #1633
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_steps(dictionary):
  total_steps = dictionary['summary']['steps']
  print total_steps
  #8286
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_floors(dictionary):
  total_floors = dictionary['summary']['floors']
  print total_floors
  # 34
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_sedentary_min(dictionary):
  total_mins = dictionary['summary']['sedentaryMinutes']
  print total_mins
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  #1020
  model.session.add()
  model.session.commit()


def load_lightly_active_min(dictionary):
  total_mins = dictionary['summary']['lightlyActiveMinutes']
  print total_mins
  #70
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_fairly_active_min(dictionary):
  total_mins = dictionary['summary']['fairlyActiveMinutes']
  print total_mins
  #51
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_very_active_min(dictionary):
  total_mins = dictionary['summary']['veryActiveMinutes']
  print total_mins
  #43
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def  load_bmr(dictionary):
  bmr = dictionary['summary']['caloriesBMR']
  print bmr
  #1118
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()


def load_activity_cals(dictionary):
  activity_cals = dictionary['summary']['activityCalories']
  print activity_cals
  #670
  miles_updated = model.Activity(id = None, user_id = None, floors = None, steps = None, sedentary_min = None, lightly_active_min = None, fairly_active_min = None, very_active_min = None, total_cal = None, bmr = None, activity_cals = None, distance = miles, date = None)
  model.session.add()
  model.session.commit()

# if I want to format the datetime object in db, do the below in a function
# time_from_column = row[index into row]
# format_time = datetime.strptime(time_from_column, "%d-%b-%Y")

def all_funs():
  load_calories(user_info)
  load_activity_cals(user_info)
  load_bmr(user_info)
  load_very_active_min(user_info)
  load_fairly_active_min(user_info)
  load_lightly_active_min(user_info)
  load_sedentary_min(user_info)
  load_floors(user_info)
  load_steps(user_info)
  # load_miles(user_info)

all_funs()