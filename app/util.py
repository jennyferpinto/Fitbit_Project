import model
import datetime
import json

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
  # today = datetime.datetime.today()
  # days = []
  # for i in range(7):
  #   days.append(today - datetime.timedelta(days=i))
  # date = days[1]
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
    formatted_time = dates.strftime('%s')
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


def patients_weekly_steps(query):
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id).limit(7)
  steps = weekly_steps(query)
  # dates = dates_for_week(all_user_activity)
  # have to put 0-however many bars in the x-axis for the graph to render
  data_steps = [
      { 'x': 0, 'y': steps[0] },
      { 'x': 1, 'y': steps[1] },
      { 'x': 2, 'y': steps[2] },
      { 'x': 3, 'y': steps[3] },
      { 'x': 4, 'y': steps[4] },
      { 'x': 5, 'y': steps[5] },
      { 'x': 6, 'y': steps[6] }
      ]
  # data_step_tuples = steps_by_day(all_user_activity)
  # data_steps = [ {"x": int(t[0]), "y": t[1]} for t in data_step_tuples]
  jsonified_steps_data = json.dumps(data_steps)
  weekly_steps_data = jsonified_steps_data.replace('"','')
  return weekly_steps_data

def patients_weekly_floors(query):
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id).limit(7)
  floors = weekly_floors(query)
  data_floors = [
      { 'x': 0, 'y': floors[0] },
      { 'x': 1, 'y': floors[1] },
      { 'x': 2, 'y': floors[2] },
      { 'x': 3, 'y': floors[3] },
      { 'x': 4, 'y': floors[4] },
      { 'x': 5, 'y': floors[5] },
      { 'x': 6, 'y': floors[6] }
      ]
  jsonified_floors_data = json.dumps(data_floors)
  weekly_floors_data = jsonified_floors_data.replace('"','')
  return weekly_floors_data

def patients_weekly_miles(query):
  # all_user_activity = model.session.query(Activity).order_by(Activity.date.desc()).filter(Activity.user_id == current_user_id).limit(7)
  miles = weekly_miles(query)
  data_miles = [
      { 'x': 0, 'y': miles[0] },
      { 'x': 1, 'y': miles[1] },
      { 'x': 2, 'y': miles[2] },
      { 'x': 3, 'y': miles[3] },
      { 'x': 4, 'y': miles[4] },
      { 'x': 5, 'y': miles[5] },
      { 'x': 6, 'y': miles[6] }
      ]
  jsonified_miles_data = json.dumps(data_miles)
  weekly_miles_data = jsonified_miles_data.replace('"','')
  return weekly_miles_data

def day_view(query):
  days_activity = query
  floors = days_activity.floors
  steps = days_activity.steps
  distance = days_activity.distance
  time_object = days_activity.date
  string_time = str(time_object)
  daily_dataset = [
      {'x': 0, 'y': floors},
      {'x': 1, 'y': steps},
      {'x': 2, 'y': distance},
      ]
  jsonified_daily_data = json.dumps(daily_dataset)
  daily_data = jsonified_daily_data.replace('"','')
  return daily_data