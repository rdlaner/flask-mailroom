#!/usr/bin/env python3
"""Main flask app"""
import os
import base64
import decimal
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('donations'))


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
