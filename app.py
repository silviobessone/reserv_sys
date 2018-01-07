from flask import Flask, render_template, make_response, request
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
    allergies = orm.Optional(str)
    notes = orm.Optional(str)
    n_reservations = orm.Optional(str)


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
def show_payment_method(n):
    payment_m = Payment_method.get(id=n)
    return payment_m


@orm.db_session
def add_payment_method(name):
    Payment_method(nome=name)


@orm.db_session
def show_reservations():
    data = db.select("SELECT * FROM Reservation")
    return data


@orm.db_session
def add_reservation(check_in,
                    check_out,
                    guest_id,
                    offer_id,
                    room,
                    subtot,
                    payment,
                    dep_val='_',
                    extra_serv_id='1',
                    voucher_id='_',
                    pagato=False,
                    dep_tx='_'):
    extra_serv_id = show_extra_serv(extra_serv_id)
    Reservation(data_check_in=check_in,
                data_check_out=check_out,
                deposit_value=dep_val,
                deposit_tx=dep_tx,
                guest_id=guest_id,
                offer_id=offer_id,
                extra_services_id=extra_serv_id,
                voucher_id=voucher_id,
                room=room,
                payment_method=payment,
                pagato=pagato,
                Totale_prov=subtot
                )
    return "OK"


@orm.db_session
def add_guest(name,
              surname,
              email,
              phone,
              name2='_',
              cognome2='_',
              phone2='_',
              allergies='_',
              notes='_',
              n_reserv=1):
    Guest(nome=name,
          cognome=surname,
          nome_accompagnate=name2,
          cognome_accompagnate=cognome2,
          email=email,
          telefono=phone,
          telefono_opt=phone2,
          notes=notes,
          n_reservations=1,
          )
    return "data"


@orm.db_session
def show_extra_serv(n):
    extra_s = Extra_services[n]
    return extra_s


@orm.db_session
def show_guest(n):
    guest = Guest[n]
    return guest


@orm.db_session
def show_offer(n):
    offer = Offer[n]
    return offer


"""RESTFUL METHODS"""


class Payment(Resource):
    def get(self):
        ppp = show_payment_method(1)
        header = {'Content-Type': 'text/html'}
        data = {
            "my_string": ppp.nome,
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
            }
        return make_response(render_template(
               'template.html', **data), 200, header
               )

    def post(self):
        req = request.form.get('nome')
        print(dir(req))
        add_payment_method(req)
        header = {'Content-Type': 'text/html'}
        data = {
            "my_string": req,
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
            }
        return make_response(render_template(
               'template.html', **data), 201, header
               )


class Home(Resource):
    def get(self):
        return {'hello': 'world'}


class Template_test(Resource):
    def get(self):
        header = {'Content-Type': 'text/html'}
        data = {
                "my_string": "Chocolate",
                "my_list": ["C", "H", "O", "C", "O", "L", "A", "T", "E"]
                }
        print(data)
        return make_response(render_template(
               'test.html', **data), 200, header
               )


class Reservations(Resource):
    def get(self):
        header = {'Content-Type': 'text/html'}
        data = show_reservations()
        def rearrange_reserv(data):
            """[(1, '2017-12-10', '2017-12-11', 500,
                'A5056086754', 1, 1, None, 1, 1, None, 1, 100)]"""
            # dict_in = {'0': 'resv_id', '1': 'ciok-in', '2': 'ciok-out',
            #            '3': 'deposit_value', '4': 'deposit_tx', '5': 'guest_id',
            #            '6': 'offer_id', '7': 'extra_serv', '8': 'voucher_id',
            #            '9': 'room', '10': 'payment', '11': 'anticipo',
            #            '12':'Totale_prov'
            #            }
            # dict_out = {'room': 0, 'nome': 1, 'cognome': 2, 'nome2': 3,
            #             'cognome2': 4, 'email': 5, 'ciok-in': 6, 'ciok-out': 7,
            #             'telf': 8, 'allergie': 9, 'altro': 10, 'voucher': 11,
            #             'resv_id': 12
            #             }
            lista_raw = list(range(0,19))
            lista_end = list()
            for tupla in data:
                lista = lista_raw
                for i,v in enumerate(tupla):
                    if i == 0:
                        lista[15] = v
                    if i == 1:
                        lista[6] = v
                    if i == 2:
                        lista[7] = v
                    if i == 3:
                        lista[16] = v
                    if i == 4:
                        lista[17] = v
                    if i == 5:
                        guest = show_guest(v)
                        lista[1] = guest.nome
                        lista[2] = guest.cognome
                        lista[3] = guest.nome_accompagnate
                        lista[4] = guest.cognome_accompagnate
                        lista[5] = guest.email
                        lista[10] = guest.telefono
                        lista[11] = guest.allergies
                        lista[12] = guest.notes
                    if i == 6:
                        lista[8] = show_offer(v)
                    if i == 7:
                        """See how to ask SET in Pony Orm """
                        lista[9] = v
                    if i == 8:
                        lista[14] = v
                    if i == 9:
                        lista[0] = v
                    if i == 10:
                        lista[18] = show_payment_methods(v)
                    lista_end.append(tuple(lista))
                return lista_end
        data = rearrange_reserv(data)

        table = {'table': data}
        return make_response(render_template(
               'reservations.html', **table), 200, header
               )

    def post(self):
        data_check_in = request.form.get('data_check_in')
        check_out = request.form.get('data_check_out')
        dep_val = request.form.get('deposit_value')
        dep_tx = request.form.get('deposit_tx')
        guest_id = request.form.get('guest_id')
        offer_id = request.form.get('offer_id')
        extra_serv_id = request.form.get('extra_services_id')
        voucher_id = request.form.get('voucher_id')
        room = request.form.get('room')
        payment = request.form.get('payment_method')
        pagato = request.form.get('pagato')
        subtot = request.form.get('Totale_prov')
        add_reservation(check_in=data_check_in,
                        check_out=check_out,
                        guest_id=guest_id,
                        offer_id=offer_id,
                        room=room,
                        subtot=subtot,
                        payment=payment,
                        dep_val=dep_val,
                        extra_serv_id=extra_serv_id,
                        voucher_id=voucher_id,
                        pagato=pagato,
                        dep_tx=dep_tx
                        )
        header = {'Content-Type': 'text/html'}
        data = {
                "url": payment
                }
        return make_response(render_template(
               'reservations.html', **data), 200, header
                )

"""ENDPOINTS"""

api.add_resource(Home, "/")
api.add_resource(Template_test, "/test")
api.add_resource(Payment, "/payment")
api.add_resource(Reservations, "/reservations")


if '__name__' == '__main__':
    app.run(debug=True)
