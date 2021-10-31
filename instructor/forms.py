from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
   instID = IntegerField('instID', validators=[DataRequired(message="must be integer"), NumberRange(min=10000000, max=99999998, message="must be 8 digit")])
   password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Register')

class LoginForm(FlaskForm):
   instID = IntegerField('instID', validators=[DataRequired(message="must be integer"), NumberRange(min=10000000, max=99999998, message="must be 8 digit")])
   password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
   submit = SubmitField('Login')


class AccountForm(FlaskForm):
   firstname = StringField('First Name', validators=[DataRequired(), Length(max=20)])
   lastname = StringField('Last Name', validators=[Length(max=20)])
   email = EmailField('College email', validators=[DataRequired(), Email()])
   address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
   gender = StringField('Gender')
   yearEnrolled = StringField('Year Enrolled')
   DOB = StringField('DOB')
   deptID = StringField('deptID')
   profilepic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
   submit = SubmitField('Update')