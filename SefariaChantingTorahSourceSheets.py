# -*- coding: utf-8 -*

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, CreateForm
from sourcesheet_actions import customize
from sefaria_functions import generate_sheet

from flask_recaptcha import ReCaptcha # Import ReCaptcha object

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter

s_sheets = [
    {
        'Torah_Verses':'Exodus 1:10',
        'Created_By': 'vmonaco',
        'Created_On': 'July 11, 2021'
        },
    {
        'Torah_Verses':'Genesis 2:11-13',
        'Created_By': 'amp',
        'Created_On': 'May 8, 2021'
        },
    {
        'Torah_Verses':'Numbers 5:23-24',
        'Created_By': 'dpolk',
        'Created_On': 'March 1, 2021'
        }
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', s_sheets=s_sheets)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/create', methods=['GET','POST'])
def create():
    form=CreateForm()

    if request.method == 'POST': # Check to see if flask.request.method is POST
        if recaptcha.verify(): # Use verify() method to see if ReCaptcha is filled out
            if form.validate_on_submit():

                Book = form.Torah_Book_Field.data
                Chapter = form.chapter.data
                StartVerse = form.startingVerse.data
                EndVerse = form.endingVerse.data

                generate_sheet(Book, Chapter, StartVerse, EndVerse)

                #flash('Sefaria Feedback: ' + query_Sefaria_Reference(verse) ,'success')
                #return redirect(url_for('create'))

                #flash(customize(verse))
                #return redirect(url_for('home'))
        else:
                flash('If you are not a robot, go ahead and check the box.')
    return render_template('create.html', title='Create Source Sheet', form=form)

