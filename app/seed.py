import model
import datetime
import fitbit
from datetime import date
import datetime

# hard coded me as a user
# figure out how to do oAuth and sync multiple users

user = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90', 'e2b38ed6dad443e8bad8efbe3e0e3da5', user_key="5fec83e8ad9ea52dd63b47a42b87b852", user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")

user_info = user.activities('2013-04-12')
user_info2 = user.activities('2013-04-11')
user_info3 = user.activities('2013-04-10')
user_info4 = user.activities('2013-04-09')

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
  model.session.add(everything_updated)
  model.session.commit()

insert_activities(user_info)
insert_activities(user_info2)
insert_activities(user_info3)
insert_activities(user_info4)