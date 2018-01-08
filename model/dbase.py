from datetime import date
from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from model.db_sessions import Manager
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

class Manager(object):
    @orm.db_session
    def show_payment_method(n):
        payment_m = Payment_method[n]
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


    @orm.db_session
    def show_voucher(n):
        voucher = Voucher[n]
        return voucher
