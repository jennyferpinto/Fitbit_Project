import model
import datetime
import fitbit

# write a script that grabs the fitbit data for the day

# take the nested dictionary and pull it apart

# nested_dict = the data pulled from c = fitbit.Fitbit('c91f84cd10f04cebad9beb7d4812eb90', 'e2b38ed6dad443e8bad8efbe3e0e3da5', user_key="5fec83e8ad9ea52dd63b47a42b87b852", user_secret="de3c9fd790a85a307c6b0ff8e0f0858d")


def load_activity():
  #index into the dictionary
  for key, value in nested_dict.iteritems():

  distance_miles = nested_dictionary['summary']['distances'][0]
  distance_miles['distance']