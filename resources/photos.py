from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)


import models


photo_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'description': fields.String,
    'camera': fields.String,
    'category': fields.String
}

class PhotoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'title',
            required=False,
            help='No photo title provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'url',
            required=False,
            help='No photo url provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'description',
            required=False,
            help='No photo description provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'camera',
            required=False,
            help='No photo camera provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'category',
            required=False,
            help='No photo category provided',
            location=['form', 'json']
        )

        super().__init__()


    def get(self):
        new_photos = [marshal(photo, photo_fields) for photo in models.Photo.select()]
        print(new_photos)

        return new_photos

    @marshal_with(photo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, '<-----args (req.body)')
        photo = models.Photo.create(**args)
        print(photo, '<------', type(photo))
        return (photo, 201)


class Photo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        
        self.reqparse.add_argument(
            'title',
            required=False,
            help='No photo title provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'url',
            required=False,
            help='No photo url provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'description',
            required=False,
            help='No photo description provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'camera',
            required=False,
            help='No photo camera provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'category',
            required=False,
            help='No photo category provided',
            location=['form', 'json']
        )

        super().__init__()

    @marshal_with(photo_fields)
    def get(self, id):

        try:
            photo = models.Photo.get(models.Photo.id==id)
        except models.Photo.DoesNotExist:
            abort(404)
        else:
            return (photo, 200)

    @marshal_with(photo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Photo.update(**args).where(models.Photo.id==id)
        query.execute()
        print(query, "<---this is query")
        return (models.Photo.get(models.Photo.id==id), 204)

    def delete(self, id):
        query = models.Photo.delete().where(models.Photo.id==id)
        query.execute()
        return {"message": "resource deleted"}

photos_api = Blueprint('resources.photos', __name__)

api = Api(photos_api)

api.add_resource(
    PhotoList,
    '/'
)
api.add_resource(
    Photo,
    '/<int:id>'
)