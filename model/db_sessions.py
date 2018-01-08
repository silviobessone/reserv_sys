from pony import orm

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
