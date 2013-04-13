from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime

# leave as None to manually connect and create tables
# would then use:
# engine = create_engine("postgresql:///fitbit_db", echo = True)
# then:
# Base.metadata.create_all(engine)

# ENGINE = None
# SESSION = None

# always connected
engine = create_engine("postgresql:///fitbit_db", echo = True)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class Users(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True)
  email = Column(String(100))
  password = Column(String(20))
  first_name = Column(String(20))
  last_name = Column(String(20))
  last_login = Column(DateTime, default = datetime.datetime.now())
  number_logins = Column(Integer)
  role = Column(String(20))
  user_key = Column(String(50), nullable = True)
  user_secret = Column(String(50), nullable = True)
  activities = relationship("Activity", backref = "user")


class Activity(Base):
  __tablename__ = "activities"

  id = Column(Integer, primary_key = True)
  user_id = Column(Integer, ForeignKey('users.id'))
  floors = Column(Integer)
  steps = Column(Integer)
  sedentary_min = Column(Integer)
  lightly_active_min = Column(Integer)
  fairly_active_min = Column(Integer)
  very_active_min = Column(Integer)
  total_cal = Column(Integer)
  bmr = Column(Integer)
  activity_cals = Column(Integer)
  distance = Column(Float)
  date = Column(Integer)


# class Therapist(Base):
#   __tablename__ = "therapists"

#   id = Column(Integer, primary_key = True)
#   email = Column(String(100))
#   password = Column(Integer)
#   first_name = Column(String(20))
#   last_name = Column(String(20))
#   last_login = Column(Integer)
#   number_logins = Column(Integer)
#   patients = relationship("Patient", backref = "therapist")


# class Patient (Base):
#   __tablename__ = "patients"

#   id = Column(Integer, primary_key = True)
#   therapist_id = Column(Integer, ForeignKey('therapists.id'))
#   email = Column(String(100))
#   password = Column(Integer)
#   first_name = Column(String(20))
#   last_name = Column(String(20))
#   last_login = Column(Integer)
#   number_logins = Column(Integer)
#   user_key = Column(String(50))
#   user_secret = Column(String(50))
#   activities = relationship("Activity", backref = "patient")


# if __name__ == "__main__":
#   main()