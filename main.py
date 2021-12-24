from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


"""
Change how you get person_id

Account for invalid id's and other errors
"""

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)

class BirthdayModel(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    birthday = db.Column(db.String(100), nullable = False)
    phone_number = db.Column(db.String(100), nullable = True)

    def __repr__(self):

        return f"Id: {self.id}, Name: {self.name}, Birthday: {self.birthday}, Phone Number: {self.phone_number}"

#Validate Request forms
person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Name Required", required=True)
person_put_args.add_argument("birthday", type=str, help="Birthday Required", required=True)
person_put_args.add_argument("phone_number", type=str, help="")


person_patch_args = reqparse.RequestParser()
person_patch_args.add_argument("name", type=str, help="Name")
person_patch_args.add_argument("birthday", type=str, help="Birthday")
person_patch_args.add_argument("phone_number", type=str, help="Phone Number")

#Converting sql alchemy objects to JSON serializable objects
resource_fields = {

    "id": fields.Integer,
    "name": fields.String,
    "birthday": fields.String,
    "phone_number": fields.String
}

#API Resources
class People(Resource):

    @marshal_with(resource_fields)
    def get(self):

        result = BirthdayModel.query.all()

        return result

    @marshal_with(resource_fields)
    def put(self):
        
        if not len(BirthdayModel.query.all()):

            person_id = 0

        else:

            person_id = max(BirthdayModel.query.all(), key = lambda x: x.id).id + 1

        args = person_put_args.parse_args()

        birthdayPerson = BirthdayModel(id = person_id, name = args["name"], birthday = args["birthday"], phone_number = args["phone_number"])

        db.session.add(birthdayPerson)
        db.session.commit()

        return birthdayPerson, 201


class Person(Resource):

    @marshal_with(resource_fields)
    def get(self, person_id):

        result = BirthdayModel.query.filter_by(id = person_id).first()

        return result, 200


    def delete(self, person_id):

        BirthdayModel.query.filter_by(id = person_id).delete()
        db.session.commit()

        return "", 204

    @marshal_with(resource_fields)
    def patch(self, person_id):

        args = person_patch_args.parse_args()
        result = BirthdayModel.query.filter_by(id = person_id).first()

        if args["name"]:

            result.name = args["name"]

        if args["birthday"]:

            result.birthday = args["birthday"]

        if args["phone_number"]:

            result.phone_number = args["phone_number"]

        db.session.commit()

        return result, 204



api.add_resource(People, "/people")
api.add_resource(Person, "/people/<int:person_id>")


if __name__ == "__main__":

    app.run(debug=True)
