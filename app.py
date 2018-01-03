from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from model.dbase import db


app = Flask(__name__)

api = Api(app)

"""TODO: Use the properly form of pony orm""" 
# @app.before_request
# def database_connect():
#     if db.is_closed():
#         database.connect()


# @app.teardown_request
# def database_disconnect(response):
#     if not database.is_closed():
#         db.close()
#     return response

class home(Resource):
    def get(self):
        return {'hello': 'world'}


class template_test(Resource):
    def get(self):
        header = {'Content-Type': 'text/html'}
        data = {
                "my_string": "Chocolate!",
                "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
                }
        return make_response(render_template('template.html', **data), 200, header)

api.add_resource(home, "/")
api.add_resource(template_test, "/test")


if '__name__' == '__main__':
    app.run(debug=True)
