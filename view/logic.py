from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from model.db_sessions import db, Manager
from pony import orm

"""RESTFUL METHODS"""


class Payment(Resource):
    def get(self):
        ppp = Manager.show_payment_method()
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
        Manager.add_payment_method(req)
        header = {'Content-Type': 'text/html'}
        data = {
            "my_string": req,
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
            }
        return make_response(render_template(
               'template.html', **data), 201, header)


class Home(Resource):
    def get(self):
        header = {'Content-Type': 'text/html'}
        data = {}
        return make_response(render_template(
               'index.html', **data), 200, header)


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
    def rearrange_reserv(self, data):
        lista_raw = list(range(0, 18))
        lista_end = list()
        for tupla in data:
            lista = lista_raw
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
                    guest = Manager.show_guest(self, n=v)
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
                    lista[8] = Manager.show_offer(self, n=v)
                if i == 7:
                    # Voucher
                    voucher = Manager.show_voucher(self, n=v)
                    lista[13] = voucher.numero
                if i == 8:
                    # ROOM
                    lista[0] = v
                if i == 9:
                    # Payment_method
                    payment_method = Manager.show_payment_method(self, n=v)
                    lista[17] = payment_method.nome
                    print(lista)
                    lista_end.append(tuple(lista))
        print(lista)
        return lista_end


    def get(self):
        if request.method == 'GET':
            header = {'Content-Type': 'text/html'}
            data = Manager.show_reservations()
            # data = Reservations.rearrange_reserv(self, data=data)
            table = {'table': data}
            return make_response(render_template(
                   'reservations.html', **table), 200, header
                   )

    def post(self):
        if request.method == 'POST':
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
            data = Manager.add_reservation(self,
                                    check_in=data_check_in,
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
                                    dep_tx=dep_tx,
                                    )
            header = {'Content-Type': 'text/html'}
            return make_response(render_template(
                   'reservations.html', **data), 200, header
                )

class Guest(Resource):
    def get(self):
        header = {'Content-Type': 'text/html'}
        req = request.form.get('id')
        import pdb; pdb.set_trace()
        if req is None:
            data = Manager.show_guest("False")
        else:
            data = Manager.show_guest(req)
        table = {"table" : data}
        return make_response(render_template(
               'guest.html', **table), 200, header
                )

    def post(self):
        req = request.form.get('nome')
        Manager.add_payment_method(req)
        header = {'Content-Type': 'text/html'}
        data = {
            "my_string": req,
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
            }
        return make_response(render_template(
               'template.html', **data), 201, header)
