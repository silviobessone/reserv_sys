from datetime import date
from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from pony import orm

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

class insert_payment(Resource):
    def get(self):
        @orm.db_session
        def print_payment_methods():
            p = Payment_method[1]
            print(p.nome)
            return make_response(render_template(
               'template.html', my_string=p.nome), 200, header
               )

    def post(self):
        @orm.db_session
        def insert_payment():
            guest = {
                    "nome": "Mario",
                    "cognome": "Rossi",
                    "nome_accompagnate": "Mayra",
                    "cognome_accompagnate": "Perez",
                    "email": "mario@email.com",
                    "telefono": "45087234", 
                    }
            Payment_method(nome="Stripe")
