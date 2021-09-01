# -*- coding: utf-8 -*

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, CreateForm
from sourcesheet_actions import customize
from sefaria_functions import generate_sheet

from flask_recaptcha import ReCaptcha # Import ReCaptcha object

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter


@app.route('/', methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    form=CreateForm()

    if request.method == 'POST': # Check to see if flask.request.method is POST
        if recaptcha.verify(): # Use verify() method to see if ReCaptcha is filled out
            if form.validate_on_submit():

                Book = form.Torah_Book_Field.data
                Chapter = form.chapter.data
                StartVerse = form.startingVerse.data
                EndVerse = form.endingVerse.data

                aliyah_ending = form.aliyah.data

                generate_sheet(Book, Chapter, StartVerse, EndVerse, aliyah_ending)

                return redirect(url_for('submission_info'))
        else:
                flash('If you are not a robot, go ahead and check the box.')
    return render_template('home.html', title='Create Source Sheet', form=form)

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

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html', title='Roadmap')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/submission_info')
def submission_info():
    return render_template('submission_info.html', title='Submission Info')

@app.route('/privacy_terms')
def privacy_terms():
    return render_template('privacy_terms.html', title='Roadmap')
