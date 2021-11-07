from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email
from wtforms.fields.html5 import EmailField


class EnrollmentForm(FlaskForm):
   course_id = StringField('Course ID', validators=[DataRequired()])
   enroll = SubmitField('Enroll')  
