from pony import orm
from model.dbase import (db, Guest, Offer, Payment_method, Room,
	                     Extra_services, Voucher, Reservation)

class Manager(object):
    # FROM PAYMENT ENDPOINT
    @orm.db_session
    def show_payment_method(self, n):
        payment_m = Payment_method[n]
        return payment_m


    @orm.db_session
    def add_payment_method(self, name):
        Payment_method(nome=name)


    # FROM RESERVATIONS ENDPOINT
    @orm.db_session
    def show_reservations():
        """GET"""
        data = db.select("SELECT * FROM Reservation")
        return data


    @orm.db_session
    def add_reservation(self, check_in,
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
        """POST"""
        extra_s = Manager.show_extra_serv(self, n=extra_serv_id)
        Reservation(data_check_in=check_in,
                    data_check_out=check_out,
                    deposit_value=dep_val,
                    deposit_tx=dep_tx,
                    guest_id=guest_id,
                    offer_id=offer_id,
                    extra_services_id=extra_s,
                    voucher_id=voucher_id,
                    room=room,
                    payment_method=payment,
                    pagato=pagato,
                    Totale_prov=subtot
                    )
        return "OK"


    @orm.db_session
    def deactivate_reservation(self):
        """PUT"""
        pass


    @orm.db_session
    def add_guest(self, name,
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
    def show_extra_serv(self, n):
        extra_s = Extra_services[n]
        return extra_s


    @orm.db_session
    def show_guest(self, n):
        guest = Guest[n]
        return guest


    @orm.db_session
    def show_offer(self, n):
        offer = Offer[n]
        return offer


    @orm.db_session
    def show_voucher(self, n):
        voucher = Voucher[n]
        return voucher
