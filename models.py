import datetime

from peewee import *

DATABASE = SqliteDatabase('photos.sqlite')

class Photo(Model):
    title = CharField()
    category = CharField()