#!/usr/bin/env python3
"""Flask-Mailroom setup script"""
import random
from flask_bcrypt import Bcrypt
from model import db, Donor, Donation


def main():
    """Main function for populating the database"""
    donors = [('Toni Morrison', random.sample(range(100, 25000), 3)),
              ('Mike McHargue', random.sample(range(100, 25000), 3)),
              ("Flannery O'Connor", random.sample(range(100, 25000), 3)),
              ('Angelina Davis', random.sample(range(100, 25000), 3)),
              ('Bell Hooks', random.sample(range(100, 25000), 3))]

    db.connect()
    db.drop_tables([Donor, Donation])
    db.create_tables([Donor, Donation])
    bcrypt = Bcrypt()

    for donor, donations in donors:
        Donor.create(name=donor,
                     email='.'.join(donor.lower().split()) + '@gmail.com',
                     password=bcrypt.generate_password_hash('password'),
                     total=sum(donations),
                     average=sum(donations) / len(donations))

    for donor, donations in donors:
        for donation in donations:
            Donation.create(donor=donor,
                            amount=donation)


if __name__ == '__main__':
    main()
