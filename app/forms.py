from flask.ext.wtf import Form, TextField, BooleanField, PasswordField
from flask.ext.wtf import Required
from wtforms import validators as v


class LoginForm(Form):
  email = TextField('email',
                    validators = [Required(), v.Email()])
  password = PasswordField('password',
                            validators = [Required()])
  # remember_me = BooleanField('remember_me', default = False)


class SignUpForm(Form):
  first_name = TextField('first_name',
                        validators=[Required()])
  last_name = TextField('last_name',
                        validators=[Required()])
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
