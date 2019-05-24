import datetime

from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('photos.sqlite')

class Photo(Model):
    title = CharField()
    category = CharField()


class User(UserMixin, Model):
    username    = CharField(unique=True)
    email       = CharField(unique=True)
    first_name  = CharField(unique=True)
    last_name   = CharField(unique=True)
    password    = CharField()

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, username,email,full_name,password,**kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username = username,email=email)
            user.password = (password)
            user.save()
            return user
        else:
            return "user with that email exists"


def initialize():
    DATABASE.connect() 
    DATABASE.close()