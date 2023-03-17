from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField,\
    SubmitField, SelectMultipleField
# from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError



class BookForm(FlaskForm):

    title = StringField("Название", validators=[DataRequired()])
    year = IntegerField('Год издания', validators=[DataRequired()])
    authors = SelectMultipleField('Автор(ы)', choices=[], default=[], coerce=int)
    publishers = SelectMultipleField('Издатель(и)', choices=[], default=[], coerce=int)

    submit = SubmitField('Сохранить')

    def set_author_choices(self, choices_list: list):
        self.authors.choices = choices_list


class AuthorForm(FlaskForm):

    fio = StringField("ФИО", validators=[DataRequired()])

    submit = SubmitField('Сохранить')


class PublisherForm(FlaskForm):

    name = StringField("Название", validators=[DataRequired()])

    submit = SubmitField('Сохранить')
