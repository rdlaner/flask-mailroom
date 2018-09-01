#!/usr/bin/env python3
"""Main flask app"""
import os
import decimal
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import Donation, Donor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('donations'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None

    if request.method == 'POST':
        user_input = request.form['username']
        pass_input = request.form['password']

        query = Donor.select().where(Donor.name == user_input)
        if query:
            if pbkdf2_sha256.verify(pass_input, query.get().password):
                session['user'] = user_input
                return redirect(url_for('add_donation'))
            else:
                login_error = 'Invalid password'
        else:
            login_error = f'Unknown username: "{user_input}"'

    return render_template('login.html', login_error=login_error)


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
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        input_donor = request.form['donor']
        input_donation = request.form['donation']

        # Create new donation in database
        Donation.create(donor=input_donor, amount=input_donation)

        # Assign new donation to donor
        try:
            donor = Donor.get(Donor.name == input_donor)
        except Donor.DoesNotExist:
            donor = Donor.create(name=input_donor, total=0, average=0)

        donor.total += decimal.Decimal(input_donation)
        donor.average = donor.total / len(donor.donations)
        donor.save()

        return redirect(url_for('home'))

    return render_template('add_donation.html')


@app.route('/account', methods=['GET'])
def account():
    if 'user' not in session:
        return redirect(url_for('login'))

    donor = Donor.get(Donor.name == session['user'])
    return render_template('account.html', donor=donor)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
