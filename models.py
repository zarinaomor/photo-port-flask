import datetime

from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('photos.sqlite')

class Photo(Model):
    title = CharField()
    category = CharField()
    # created_by = ForeignKeyField(User, related_name='photo_set')
    # created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
    
    # @classmethod
    # def create_photo(cls, id,title,url,description,camera,category,**kwargs):
    #     email = email.lower()
    #     try:
    #         cls.select().where(
    #             (cls.email==email)
    #         ).get()
    #     except cls.DoesNotExist:
    #         user = cls(username = username,email=email)
    #         user.password = (password)
    #         user.save()
    #         return user
    #     else:
    #         return "user with that email exists"


class User(UserMixin, Model):
    username    = CharField(unique=True)
    email       = CharField(unique=True)
    password    = CharField()

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, username,email,password,**kwargs):
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
    DATABASE.create_tables([User], safe=True)
    DATABASE.create_tables([Photo], safe=True)
    DATABASE.close()