from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, IntegerField, FloatField, DateField, SelectField, QuerySelectField
from flask.ext.wtf import Required
from wtforms import validators as v
import model
import util


class LoginForm(Form):
  email = TextField('email',
                    validators = [Required(), v.Email()])
  password = PasswordField('password',
                            validators = [Required()])
  # remember_me = BooleanField('remember_me', default = False)


class SignUpTherapistForm(Form):
  first_name = TextField('first_name',
                        validators=[Required()])
  last_name = TextField('last_name',
                        validators=[Required()])
  role = SelectField('role',
                  validators=[Required()],
                  choices=[('therapist', 'Therapist'), ('patient', 'Patient')])
  # therapist_name = TextField('therapist_name')
  email = TextField('first_email',
                    validators=[Required(),
                    v.Email(),
                    v.EqualTo('confirm_email',
                    message = "Emails have to match")])
  confirm_email = TextField('Repeat Email')
  password = PasswordField('first_password',
                          validators = [Required(),
                          v.EqualTo('confirm_password',
                          message = 'Passwords must match')])
  confirm_password = PasswordField('Repeat Password')


class SignUpPatientForm(Form):
  first_name = TextField('first_name',
                        validators=[Required()])
  last_name = TextField('last_name',
                        validators=[Required()])
  role = SelectField('role',
                  validators=[Required()],
                  choices=[('therapist', 'Therapist'), ('patient', 'Patient')])
  # therapist_name = TextField('therapist_name')
  email = TextField('first_email',
                    validators=[Required(),
                    v.Email(),
                    v.EqualTo('confirm_email',
                    message = "Emails have to match")])
  confirm_email = TextField('Repeat Email')
  password = PasswordField('first_password',
                          validators = [Required(),
                          v.EqualTo('confirm_password',
                          message = 'Passwords must match')])
  confirm_password = PasswordField('Repeat Password')
  therapist = QuerySelectField(query_factory=model.session.query(model.Users).filter(model.Users.role == 'therapist').all)


class GoalsForm(Form):
  steps = IntegerField('steps',
                      validators=[Required()])
  floors = IntegerField('floors',
                      validators=[Required()])
  distance = FloatField('distance',
                      validators=[Required()])
  date = DateField('date',
                  validators=[Required()])