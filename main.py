#!/usr/bin/env python3
"""Main flask app"""
import os
import decimal
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from model import Donation, Donor
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(name):
    return Donor.select().where(Donor.name == name).first()


@app.route('/')
def home():
    return redirect(url_for('donations'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)\
                            .decode('utf-8')
        donor = Donor.create(name=form.username.data,
                             email=form.email.data,
                             password=hashed_pass,
                             total=0,
                             average=0)
        flash(f'Your account has been created. You may now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        donor = Donor.select().where(Donor.email == form.email.data).first()
        if donor and bcrypt.check_password_hash(donor.password, form.password.data):
            login_user(donor, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/donations')
def donations():
    donations = Donation.select()
    return render_template('donations.html', donations=donations)


@app.route('/donors')
def donors():
    donors = Donor.select()
    return render_template('donors.html', donors=donors)


@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    donor = None
    if request.method == 'POST':
        input_donation = request.form['donation']

        Donation.create(donor=current_user.name, amount=input_donation)
        current_user.total += decimal.Decimal(input_donation)
        current_user.average = current_user.total / len(current_user.donations)
        current_user.save()

        return redirect(url_for('home'))

    return render_template('add_donation.html', donor=donor)


@app.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html', title='Account', donor=current_user)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 50000))
    app.run(host='0.0.0.0', port=port, debug=True)
