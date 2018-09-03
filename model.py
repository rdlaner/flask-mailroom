#!/usr/bin/env python3
"""Peewee Database Model Definition"""
import os
from functools import partial
from peewee import Model, CharField, DecimalField, ForeignKeyField
from playhouse.db_url import connect
from flask_login import UserMixin

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))
MoneyField = partial(DecimalField, decimal_places=2)


class BaseModel(Model):
    """This class defines the base class for all Peewee data tables"""
    class Meta:
        """Meta class required for Peewee"""
        database = db


class Donor(BaseModel, UserMixin):
    """This class defines individual donors."""
    name = CharField(primary_key=True, max_length=40, unique=True, null=False)
    email = CharField(max_length=255, unique=True, null=False)
    password = CharField(max_length=255, null=False)
    total = MoneyField()
    average = MoneyField()


class Donation(BaseModel):
    """This class defines the donations made by all donors."""
    donor = ForeignKeyField(Donor, backref='donations')
    amount = MoneyField()
