import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import redirect, Blueprint, flash
from flask.helpers import url_for
from flask import Flask
from flask import render_template
from flask import request, current_app
from classes import User
from passlib.apps import custom_app_context as pwd_context

link1 = Blueprint('link1',__name__)
dsn = """user='vagrant' password='vagrant' host='localhost' port=5432 dbname='itucsdb'"""


@link1.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@link1.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        Flag = current_app.store.verify_user(request.form['uname'], request.form['psw'])
        if Flag == 0:
            return render_template('login.html', uname = request.form['uname'])
        elif Flag == -1:
            flash('Wrong password!')
        else:
            flash('No such user!')
        return redirect(url_for('link1.home_page'))
    else:
        return render_template('login.html', uname = "NoName")

@link1.route('/signup', methods = ['GET', 'POST'])
def signup():
        return render_template('signup.html')

@link1.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        userpsw0 = request.form['psw']
        userpwd1 = request.form['psw-repeat']
        if userpsw0 != userpwd1:
            flash('Passwords do not match!')
            return redirect(url_for('link1.signup'))
        else:
            userName = request.form['name']
            userNumber = request.form['studentno']
            useremail = request.form['email']
            userpsw = pwd_context.encrypt(userpsw0)
            nuser = User(userName,userNumber,useremail,userpsw)
            current_app.store.add_user(nuser)
        return render_template('home.html')