from flask import Flask
from datetime import date
from pony import orm


db = orm.Database()


class Guest(db.Entity):
    nome = orm.Required(str, 18)
    cognome = orm.Required(str)
    nome_accompagnate = orm.ptional(str)
    cognome_accompagnate = orm.Optional(str)
    email = orm.Required(str, unique=True)
    telefono = orm.Optional(str, unique=True)
    telefono_opt = orm.Optional(str)
    reservations = orm.Set('Reservation')


class Offer(db.Entity):
    nome = orm.Required(str, 24, unique=True)
    prezzo = orm.Optional(str)
    descrizione = orm.Optional(LongStr)
    reservations_id = orm.Set('Reservation')


class Payment_method(db.Entity):
    name = orm.Required(str)
    reservations_id = orm.Set('Reservation')


class Room(db.Entity):
    name = orm.Required(str)
    descripzione = orm.Optional(LongStr)
    reservations_id = orm.Set('Reservation')


class Extra_sevices(db.Entity):
    name = orm.Optional(str, 24)
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
    extra_sevicess_id = orm.Set(Extra_sevices)
    voucher_id = orm.Optional(Voucher)
    room = orm.Required(Room)
    payment_method = orm.Required(Payment_method)
    anticipo = orm.Optional(int)
    pagato = orm.Required(bool, default=False)
    Totale_prov = orm.Required(int)


db.bind(provider='sqlite', filename='demo_locanda_db.sqlite', create_db=True)
orm.sql_debug(False)
db.generate_mapping()


app = Flask(__name__)

@app.route('/')
def home():
	return "Welcome to the Cioccolocanda!"

