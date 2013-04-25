from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Float, DateTime
from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required


# # leave as None to manually connect and create tables
# # would then use:
# engine = create_engine("postgresql:///fitbit_db", echo = True)
# # then:
# Base.metadata.create_all(engine)

# ENGINE = None
# SESSION = None

# # always connected
engine = create_engine("postgresql:///fitbit_db", echo = True)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class Users(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True)
  email = Column(String(100))
  password = Column(String(255))
  first_name = Column(String(30))
  last_name = Column(String(30))
  last_login = Column(DateTime, nullable = True)
  number_logins = Column(Integer)
  role = Column(String(20), nullable = True)
  therapist = Column(Integer, nullable = True)
  user_key = Column(String(255), nullable = True)
  user_secret = Column(String(255), nullable = True)
  activities = relationship("Activity", backref = "users")
  # goals = relationship("Goal", backref = "user")

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  # def __repr__(self):
  #   return '<User %r' % (self.name)


class Activity(Base):
  __tablename__ = "activities"

  id = Column(Integer, primary_key = True)
  user_id = Column(Integer, ForeignKey('users.id'))
  floors = Column(Integer, nullable = True)
  steps = Column(Integer, nullable = True)
  sedentary_min = Column(Integer, nullable = True)
  lightly_active_min = Column(Integer, nullable = True)
  fairly_active_min = Column(Integer, nullable = True)
  very_active_min = Column(Integer, nullable = True)
  total_cal = Column(Integer, nullable = True)
  bmr = Column(Integer, nullable = True)
  activity_cals = Column(Integer, nullable = True)
  distance = Column(Float, nullable = True)
  date = Column(DateTime, nullable = True)

# class Goal(Base):
#   __tablename__ = "goals"
#   id = Column(Integer, primary_key = True)
#   user_id = Column(Integer, ForeignKey('users.id'))


# if __name__ == "__main__":
#   main()