from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=25)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=2, max=25), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=25)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateForm(FlaskForm):

    TORAH_BOOKS= [
        ('Genesis', 'Genesis'),
        ('Exodus', 'Exodus'),
        ('Leviticus', 'Leviticus'),
        ('Numbers', 'Numbers'),
        ('Deuteronomy', 'Deuteronomy')
    ]
    Torah_Book_Field= SelectField(u'What book in the Torah are you selecting?', choices=TORAH_BOOKS, validators = [Required()])


    chapter = IntegerField('Select Chapter', validators=[DataRequired()])
    startingVerse = IntegerField('Select Starting Verse', validators=[DataRequired()])
    endingVerse = IntegerField('Select Ending Verse', validators=[DataRequired()])
    aliyah = BooleanField('Last verse listed is end of an <i>aliyah</i>.', validators=[])

    submit = SubmitField('Create')