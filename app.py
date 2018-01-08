from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from model.dbase import db, Manager
from view.logic import Home, Template_test, Payment, Reservations
from pony import orm


app = Flask(__name__)

api = Api(app)

"""MODEL"""

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.sql_debug(True)
db.generate_mapping(create_tables=True)

"""ENDPOINTS"""

api.add_resource(Home, "/")
api.add_resource(Template_test, "/test")
api.add_resource(Payment, "/payment")
api.add_resource(Reservations, "/reservations")


if '__name__' == '__main__':
    app.run(debug=True)
