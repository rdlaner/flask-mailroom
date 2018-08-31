#!/usr/bin/env python3
"""Flask-Mailroom setup script"""
import random
from model import db, Donor, Donation


def main():
    """Main function for populating the database"""
    donors = [('Toni Morrison', random.sample(range(100, 25000), 3)),
              ('Mike McHargue', random.sample(range(100, 25000), 3)),
              ("Flannery O'Connor", random.sample(range(100, 25000), 3)),
              ('Angelina Davis', random.sample(range(100, 25000), 3)),
              ('Bell Hooks', random.sample(range(100, 25000), 3))]

    with db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        db.drop_tables([Donor, Donation])
        db.create_tables([Donor, Donation])

        for donor, donations in donors:
            Donor.create(name=donor,
                         total=sum(donations),
                         average=sum(donations) / len(donations))

        for donor, donations in donors:
            for donation in donations:
                Donation.create(donor=donor,
                                amount=donation)


if __name__ == '__main__':
    main()
