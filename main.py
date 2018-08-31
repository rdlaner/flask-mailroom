#!/usr/bin/env python3
"""Main flask app"""
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/all')
def all():
    donations = Donation.select()
    return render_template('donations.html', donations=donations)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
