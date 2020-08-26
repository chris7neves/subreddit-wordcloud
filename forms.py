from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

def validate_characters(form, field):
    illegal_characters = '!@#$%^&*()-_=+[]}{\\?/.>,\'\"<`~'
    for char in field.data:
        if char in illegal_characters:
            message = "Subreddit name must not contain {}".format(char)
            raise ValidationError(message)

class SubredditSelect(FlaskForm):
    subreddit = StringField('Subreddit Name', 
        validators=[DataRequired(), Length(min=1, max=22), validate_characters])
    submit = SubmitField('Data!')
