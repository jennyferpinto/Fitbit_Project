import model
import datetime
import fitbit
from datetime import date
import datetime
from util import insert_activities # imports just that function

# hard coded me as a user
# figure out how to do oAuth and sync multiple users
# store API keys in the environment later when deploying to Heroku

user = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90', 'e2b38ed6dad443e8bad8efbe3e0e3da5', user_key="5fec83e8ad9ea52dd63b47a42b87b852", user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")

user_info = user.activities('2013-04-12')
user_info2 = user.activities('2013-04-11')
user_info3 = user.activities('2013-04-10')
user_info4 = user.activities('2013-04-09')

insert_activities(user_info)
insert_activities(user_info2)
insert_activities(user_info3)
insert_activities(user_info4)