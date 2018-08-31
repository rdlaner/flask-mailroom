#!/usr/bin/env python3
"""Peewee Database Model Definition"""
import os
from functools import partial
from peewee import Model, CharField, DecimalField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))
MoneyField = partial(DecimalField, decimal_places=2)


class BaseModel(Model):
    """This class defines the base class for all Peewee data tables"""
    class Meta:
        """Meta class required for Peewee"""
        database = db


class Donor(BaseModel):
    """This class defines individual donors."""
    name = CharField(primary_key=True, max_length=40)
    total = MoneyField()
    average = MoneyField()


class Donation(BaseModel):
    """This class defines the donations made by all donors."""
    donor = ForeignKeyField(Donor, backref='donations')
    amount = MoneyField()
