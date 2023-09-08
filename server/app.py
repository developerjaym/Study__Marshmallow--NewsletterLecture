#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Newsletter, Writer, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
api = Api(app)

ma = Marshmallow(app)

class WriterSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Writer
    id = ma.auto_field()
    name = ma.auto_field()

singular_writer_schema = WriterSchema()
plural_writer_schema = WriterSchema(many=True)

class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tag
    id = ma.auto_field()
    content = ma.auto_field()

singular_tag_schema = TagSchema()
plural_tag_schema = TagSchema(many=True)

class NewsletterSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Newsletter

    id = ma.auto_field()
    title = ma.auto_field()
    published_at = ma.auto_field(data_key="publishedAt")
    writer = ma.Nested(singular_writer_schema)
    tags = ma.Pluck(TagSchema, 'content', many=True)


singular_newsletter_schema = NewsletterSchema()
plural_newsletter_schema = NewsletterSchema(many=True)


class Newsletters(Resource):
    # new way (with Marshmallow!)
    def get(self):    
        newsletters = Newsletter.query.all()
        response = make_response(
            plural_newsletter_schema.dump(newsletters),
            200,
        )
        return response
    

    # new way! (without Marshmallow!)
    def post(self):
        
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response = make_response(
            singular_newsletter_schema.dump(new_record),
            201,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):

        response_json = singular_newsletter_schema.dump(Newsletter.query.filter_by(id=id).first())

        response = make_response(
            response_json,
            200,
        )

        return response

    def patch(self, id):

        record = Newsletter.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def delete(self, id):

        record = Newsletter.query.filter_by(id=id).first()
        
        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(NewsletterByID, '/newsletters/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)