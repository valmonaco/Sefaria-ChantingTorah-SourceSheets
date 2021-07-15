from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


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

@app.route('/register')
def register():
    form=RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    return render_template('login.html', title='Login')
