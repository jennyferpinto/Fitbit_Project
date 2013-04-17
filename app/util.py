import model
import datetime

def insert_activities(dictionary):
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
  date = datetime.datetime.now()
  # date = datetime.date.today()
  everything_updated = model.Activity(id=None, user_id=None,
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