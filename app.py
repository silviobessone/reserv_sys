from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from datetime import date
from pony import orm


app = Flask(__name__)

api = Api(app)

"""MODEL"""

db = orm.Database()


class Guest(db.Entity):
    nome = orm.Required(str)
    cognome = orm.Required(str)
    nome_accompagnate = orm.Optional(str)
    cognome_accompagnate = orm.Optional(str)
    email = orm.Required(str, unique=True)
    telefono = orm.Optional(str, unique=True)
    telefono_opt = orm.Optional(str)
    reservations = orm.Set('Reservation')


class Offer(db.Entity):
    nome = orm.Required(str, unique=True)
    prezzo = orm.Optional(str)
    descrizione = orm.Optional(str)
    reservations_id = orm.Set('Reservation')


class Payment_method(db.Entity):
    nome = orm.Required(str)
    reservations_id = orm.Set('Reservation')


class Room(db.Entity):
    nome = orm.Required(str)
    descripzione = orm.Optional(str)
    reservations_id = orm.Set('Reservation')


class Extra_services(db.Entity):
    nome = orm.Optional(str)
    prezzo = orm.Optional(int)
    descripzione = orm.Optional(str)
    reservations_id = orm.Set('Reservation')


class Voucher(db.Entity):
    numero = orm.Optional(str)
    data_emizione = orm.Optional(str)
    data_scadenza = orm.Optional(str)
    attivo = orm.Required(bool, default='true')
    reservation_id = orm.Optional('Reservation')


class Reservation(db.Entity):
    data_check_in = orm.Required(date)
    data_check_out = orm.Required(date)
    deposit_value = orm.Optional(int)
    deposit_tx = orm.Optional(str)
    guest_id = orm.Required(Guest)
    offer_id = orm.Required(Offer)
    extra_services_id = orm.Set(Extra_services)
    voucher_id = orm.Optional(Voucher)
    room = orm.Required(Room)
    payment_method = orm.Required(Payment_method)
    anticipo = orm.Optional(int)
    pagato = orm.Required(bool, default=False)
    Totale_prov = orm.Required(int)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.sql_debug(True)
db.generate_mapping(create_tables=True)

"""DECORATED FUNCTIONS"""

@orm.db_session
def show_payment_methods():
    mmm = Payment_method[1]
    return mmm

@orm.db_session
def add_payment_method(name):
    Payment_method(name)


"""RESTFUL METHODS"""

class payment(Resource):
    def get(self):
        ppp = show_payment_methods()
        header = {'Content-Type': 'text/html'}
        data = {
            "my_string": ppp.nome,
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
            }
        return make_response(render_template(
               'template.html', **data), 200, header
               )

    def post(self, dict):
        data = add_payment_method(**kwargs)
        return make_response(render_template(
               'template.html', **data), 201, header      
               )


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
        return make_response(render_template(
               'template.html', **data), 200, header      
               )

"""ENDPOINT"""

api.add_resource(home, "/")
api.add_resource(template_test, "/test")
api.add_resource(payment, "/payments")


if '__name__' == '__main__':
    app.run(debug=True)
