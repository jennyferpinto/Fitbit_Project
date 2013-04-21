import model
import datetime


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
  date = datetime.datetime.utcnow()
  # date = datetime.date.today()
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

# don't want to put the insert and commit to db here, put it under views instead

def weekly_steps(user_activity_query):
  # # current_user_id = model.current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.asc()).filter(Activity.user_id == '2').limit(7)
  all_steps = user_activity_query
  index = 0
  list_steps = []
  for num in range(0,7):
    step = all_steps[index].steps
    list_steps.append(step)
    index += 1
  new_list = reversed(list_steps)
  reversed_steps = []
  for i in new_list:
    reversed_steps.append(i)
  print "*********************************"
  print reversed_steps
  print "*********************************"
  return reversed_steps


def weekly_floors(user_activity_query):
  # # current_user_id = model.current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.asc()).filter(Activity.user_id == '2').limit(7)
  all_floors = user_activity_query
  index = 0
  list_floors = []
  for num in range(0,7):
    floor = all_floors[index].floors
    list_floors.append(floor)
    index += 1
  new_list = reversed(list_floors)
  reversed_floors = []
  for i in new_list:
    reversed_floors.append(i)
  print "*********************************"
  print reversed_floors
  print "*********************************"
  return reversed_floors

def weekly_miles(user_activity_query):
  # # current_user_id = model.current_user.id
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.asc()).filter(Activity.user_id == '2').limit(7)
  all_miles = user_activity_query
  index = 0
  list_miles = []
  for num in range(0,7):
    miles = all_miles[index].distance
    list_miles.append(miles)
    index += 1
  new_list = reversed(list_miles)
  reversed_miles = []
  for i in new_list:
    reversed_miles.append(i)
  print "*********************************"
  print reversed_miles
  print "*********************************"
  return reversed_miles



def dates_for_week(date_query):
  all_dates = date_query
  index = 0
  list_dates = []
  for num in range(0,7):
    dates = all_dates[index].date
    # change date into a string instead of datetime value
    formatted_time = dates.strftime('%M %d')
    list_dates.append(formatted_time)
    index += 1
  new_list = reversed(list_dates)
  reversed_dates = []
  for i in new_list:
    reversed_dates.append(i)
  print "*********************************"
  # must format the datetime object with strptime()
  print reversed_dates
  print "*********************************"
  return reversed_dates

def rickshaw_formatter(json):
  pass