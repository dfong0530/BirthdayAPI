from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

birthdays = {}

person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Name Required", required=True)
person_put_args.add_argument("birthday", type=str, help="Birthday Required", required=True)
person_put_args.add_argument("phone_number", type=str, help="")


class People(Resource):

    def get(self):

        return birthdays

    def put(self):

        person_id = max(birthdays.keys()) + 1

        args = person_put_args.parse_args()

        birthdays[person_id] = args

        return args, 201


class Person(Resource):

    def get(self, person_id):

        if person_id not in birthdays:

            abort("No such id exits!")

        return birthdays[person_id], 200


    def delete(self, person_id):

        if person_id not in birthdays:

            abort("Id does not exist")

        del birthdays[person_id]

        return "", 204


    def patch(self, person_id):

        if person_id not in birthdays:

            abort("Id does not exist")

        for args in request.form:

            if args in birthdays[person_id]:

                birthdays[person_id][args] = request.form[args]

        return birthdays[person_id], 204

    

api.add_resource(People, "/people")
api.add_resource(Person, "/people/<int:person_id>")


if __name__ == "__main__":

    app.run(debug=False)
