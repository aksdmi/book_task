from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError



class BookForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired])
    submit = SubmitField('Submit')