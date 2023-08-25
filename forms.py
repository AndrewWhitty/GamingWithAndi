from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, FloatField
from wtforms.validators import InputRequired

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    platform = SelectField('Platform', choices=[
        ('SNES', 'SNES'),
        ('N64', 'N64'),
        # Add other platform choices
    ], validators=[InputRequired()])
    date_started = DateField('Date Started')
    date_finished = DateField('Date Finished')
    status = StringField('Status')
    release_date = DateField('Release Date')
    format = StringField('Format')
    size = FloatField('Size')
    hours_to_complete = IntegerField('Hours to Complete')
    metacritic_rating = IntegerField('Metacritic Rating')
    my_rating = IntegerField('My Rating')
