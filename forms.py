from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp


class SubjectForm(Form):
    name = StringField(
        'name'
    )


class RegisterForm(Form):
    student_id = StringField(
        'student_id'
    )
    subject_id = StringField(
        'subject_id'
    )
