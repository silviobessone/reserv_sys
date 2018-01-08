from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from model.dbase import *
from pony import orm


app = Flask(__name__)

api = Api(app)

"""MODEL"""

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.sql_debug(True)
db.generate_mapping(create_tables=True)


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
            lista_raw = list(range(0, 18))
            lista_end = list()
            for tupla in data:
                """(1, '2017-12-10', '2017-12-11', 500,
                    'A5056086754', 1, 1, None, 1, 1, None, 1, 100)
                    [1, 'Pepito', 'Perez', 'Jimena', 'Jimenez',
                    'pepito@email.com', '2017-12-10',
                    '2017-12-11', Offer[1], None, '556893657', 'Fragole',
                    '2 bambini 6-7 anni', 13, 1, 500, 'A5056086754', 'Stripe']
                """
                lista = lista_raw
                print(tupla)
                for i, v in enumerate(tupla):
                    if i == 0:
                        # resv_id
                        lista[14] = v
                    if i == 1:
                        # Ciock-in
                        lista[6] = v
                    if i == 2:
                        # Ciock-out
                        lista[7] = v
                    if i == 3:
                        # Anticipo
                        lista[15] = v
                    if i == 4:
                        # Dep_tx
                        lista[16] = v
                    if i == 5:
                        # from guest_id
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
                        # offerta
                        lista[8] = show_offer(v)
                    if i == 7:
                        # Voucher
                        voucher = show_voucher(v)
                        lista[13] = voucher.numero
                    if i == 8:
                        # ROOM
                        lista[0] = v
                    if i == 9:
                        # Payment_method
                        payment_method = show_payment_method(v)
                        lista[17] = payment_method.nome
                        print("Siguiente tupla '{}'".format(tupla))
                        print("La lista resultante {}".format(lista))
                        lista_end.append(tuple(lista))

                '''(2, '2017-12-17', '2017-12-18', 700, 'B3255086798', 2, 3,
                    None, 1, 1, None, 1, 150)'''
                print(lista_end)
                """(1, 'Manuel', 'Carreño', 'Julia', 'Guzman',
                 'm.carreno@email.com', '2017-12-10', '2017-12-11', Offer[1],
                 1, '116868468', 'Aglio', '', 13, 1, 5, 500, 'E5056086985',
                 'Stripe')"""
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
