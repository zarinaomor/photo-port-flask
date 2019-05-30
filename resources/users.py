import json

from flask import Flask,jsonify, Blueprint, abort, make_response, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models

user_fields = {
    "id":fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        new_users = [marshal(user, user_fields) for user in models.User.select()]
        return new_users

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json'] 
        )
        
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        
        super().__init__()

    
    @marshal_with(user_fields)
    def get(self, id):
        try:
            user = models.User.get(models.User.id==id)
        except models.User.DoesNotExist:
            abort(404)
        else:
            return (user, 200)

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id==id)
        query.execute()
        print(query, "<---this is query")
        return (models.User.get(models.User.id==id), 204)

    def delete(self, id):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return {"message": "resource deleted"}

class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )

        super().__init__()
        
    def post(self):
        try:
            args = self.reqparse.parse_args()
            user = models.User.get(models.User.username==args['username'])
            if(user):
                if(user.password == args['password']):
                    return make_response(
                        json.dumps({
                            'user':marshal(user, user_fields),
                            'message': "success",
                        }), 200)
                else:
                    return make_response(
                        json.dumps({
                            'message': "incorrect password"
                        }), 401)
        except models.User.DoesNotExist:
            return make_response(
                json.dumps({
                    'message': "Username does not exist"
                }), 400)  
    @marshal_with(user_fields)
    def get(self, id):
        try:
            user = models.User.get(models.User.id==id)
        except models.User.DoesNotExist:
            abort(404)
        else:
            return (user, 200)

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(**args).where(models.User.id==id)
        query.execute()
        print(query, "<---this is query")
        return (models.User.get(models.User.id==id), 204)

    def delete(self, id):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return {"message": "resource deleted"}

class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        print('User has been successfully logged out.')  
        return 'User has been successfully logged out.'    
        

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/',
)
api.add_resource(
    User,
    '/<int:id>',
)
api.add_resource(
    UserLogin,
    '/login'
)
api.add_resource(
    UserLogout,
    '/logout'
)
