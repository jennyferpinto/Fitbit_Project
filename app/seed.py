import model
import datetime
import fitbit
from datetime import date
import datetime

# nested_dict = the data pulled from c = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90', 'e2b38ed6dad443e8bad8efbe3e0e3da5', user_key="5fec83e8ad9ea52dd63b47a42b87b852", user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")
# user_info = nested_dict

user_info = {u'activities': [], u'goals': {u'floors': 10, u'caloriesOut': 2756, u'activeScore': 1000, u'steps': 10000, u'distance': 8.05}, u'summary': {u'distances': [{u'distance': 5.7, u'activity': u'total'}, {u'distance': 5.7, u'activity': u'tracker'}, {u'distance': 0, u'activity': u'loggedActivities'}, {u'distance': 3.14, u'activity': u'veryActive'}, {u'distance': 2.29, u'activity': u'moderatelyActive'}, {u'distance': 0.27, u'activity': u'lightlyActive'}, {u'distance': 0, u'activity': u'sedentaryActive'}], u'elevation': 103.63, u'sedentaryMinutes': 1020, u'lightlyActiveMinutes': 70, u'caloriesOut': 1633, u'caloriesBMR': 1118, u'marginalCalories': 477, u'fairlyActiveMinutes': 51, u'veryActiveMinutes': 43, u'activityCalories': 670, u'steps': 8286, u'floors': 34, u'activeScore': 553}}


def insert_activities(dictionary):
  #aggregated all the functions into one
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
  date = datetime.datetime.now()
  # date = datetime.date.today()
  everything_updated = model.Activity(id = None, user_id = None, floors = total_floors, steps = total_steps, sedentary_min = s_mins, lightly_active_min = la_mins, fairly_active_min = fa_mins, very_active_min = va_mins, total_cal = total_cals, bmr = bmr, activity_cals = activity_cals, distance = total_miles, date = date)
  #figure out how to get timestamp in db
  model.session.add(everything_updated)
  model.session.commit()

insert_activities(user_info)

