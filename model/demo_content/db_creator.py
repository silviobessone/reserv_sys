from datetime import date, timedelta
from pony import orm

db = orm.Database()

"""'Cam.;Lettera di conferma;Primo Nome;Secondo Nome;Telefono;Email;Dal;Al;
    Notti;Nr Ospiti;x;Pacchetto;"EXTRA; Cena con Contam. cacao;"EXTRA; Pranzo";
    "EXTRA; Corso di pasticceria";"EXTRA; Bagno nel cioccolato";
    "EXTRA; Massaggio ";"EXTRA;  Altro";Data convenz;Vaucher;Pagato;
    Lettera 'accogli.; Notte;Cena; Cena cont.cacao;Corso di pasticceria;
    Visita al museo;Attestato Tortino;Extra?;Concatena extra; Pacchetto sigla;
    Clienti;Tipo;Giorno;Mese;Anno;1;2;Sogg. Futuri;Presso;;;;;;;;;;;;;;\r\n'
"""

class Guest(db.Entity):
    nome = orm.Required(str)
    cognome = orm.Required(str)
    nome_accompagnate = orm.Optional(str)
    cognome_accompagnate = orm.Optional(str)
    email = orm.Required(str, unique=True)
    telefono = orm.Optional(str, unique=True)
    allergies = orm.Optional(str)
    notes = orm.Optional(str)
    n_reservations = orm.Optional(str)
    vouchers = orm.Set('Voucher')
    reservations = orm.Set('Reservation')


class Offer(db.Entity):
    nome = orm.Required(str, unique=True)
    prezzo = orm.Optional(int)
    descrizione = orm.Optional(str)
    voucher = orm.Optional('Voucher')
    reservations = orm.Set('Reservation')


class Payment_method(db.Entity):
    name = orm.Required(str)
    vouchers = orm.Set('Voucher')


class Room(db.Entity):
    nome = orm.Required(str)
    descrizione = orm.Optional(str)
    reservations = orm.Set('Reservation')


class Extra_services(db.Entity):
    nome = orm.Required(str)
    prezzo = orm.Required(int)
    descrizione = orm.Required(str)
    reservations = orm.Set('Reservation')


class Voucher(db.Entity):
    numero = orm.Required(int)
    data_emizione = orm.Required(date)
    data_scadenza = orm.Required(date)
    valido = orm.Required(bool, default='true')
    cliente = orm.Required(Guest)
    reservation = orm.Optional('Reservation')
    payment_method = orm.Required(Payment_method)
    oferta = orm.Set(Offer)


class Reservation(db.Entity):
    data_check_in = orm.Required(date)
    data_check_out = orm.Required(date)
    deposit_value = orm.Optional(int)
    confirmed = orm.Required(bool, default=False)
    deposit_tx = orm.Optional(str)
    anticipo = orm.Optional(int)
    pagato = orm.Required(bool, default=False)
    Totale_prov = orm.Required(int)
    voucher = orm.Optional(Voucher)
    extra_sevicess = orm.Set(Extra_services)
    room = orm.Required(Room)
    guest = orm.Required(Guest)
    offer = orm.Required(Offer)


db.bind(provider='sqlite', filename='raw_database.sqlite', create_db=True)
orm.sql_debug(True)
db.generate_mapping(create_tables=True)


dic = {'nome': 2,  'telefono': 5, 'email': 4, 'altro': 17}

c_bagno = {'nome' : 'Ciocco Bagno',
            'prezzo': 80,
            'descrizione': 'Ciocco bagno in vasca con cioccolata a 40°'}
c_cacao = {'nome': 'Cena Contaminazione Cacao',
            'prezzo': 90,
            'descrizione': 'Piatti di gastronomia Lombarda contaminati al cacao'}
c_massaggio = {'nome': 'Masaggio al cioccolato',
                'prezzo': 180,
                'descrizione': 'Massagio per coppia fatti con cioccolata'}

lista_serv = [c_bagno, c_cacao, c_massaggio]

f_div = {'nome' : 'Fuga Con divertimento',
         'prezzo': 90,
         'descrizione': 'Offerta per Smart',
         'agente': 'Smartbox'}

c_cacao = {'nome' : 'Contaminazione Cacao',
           'prezzo': 320,
           'descrizione': 'Allogio una notte, visita guidata al museo' +
                          'corso pasticeria, cena contaminazione',
           'agente': 'Smartbox'}

mille_n = {'nome' : 'Mille una note',
           'prezzo': 180,
           'descrizione': 'Allogio una notte, visita guidata al museo' +
                          'corso pasticeria',
           'agente': 'Smartbox'}

lista_offer = [f_div, c_cacao, mille_n]

ecuador = {'nome' : 'Ecuador',
           'descrizione': 'Camera arredata con elementi'+
                          'tipici di Ecuador'}

venezuela = {'nome' : 'Venezuela',
             'descrizione': 'Camera arredata con elementi'+
                          'tipici di Venezuela'}

sri_lanka = {'nome' : 'Sri Lanka',
             'descrizione': 'Camera arredata con elementi'+
                            'tipici di Sri Lanka'}

lista_room = [ecuador, venezuela, sri_lanka]

vou_1 = {'oferta_id': 1, 'data_creation': [2017,12,10],
         'numero': 1000, 'cliente': 1, 'reserv': None }

vou_2 = {'oferta_id': 2, 'data_creation': [2017,12,15],
         'numero': 1000, 'cliente': 2, 'reserv': None}

vou_3 = {'oferta_id': 1, 'data_creation': [2018,1,1],
         'numero': 1000, 'cliente': 4, 'reserv': None}

vou_4 = {'oferta_id': 3, 'data_creation': [2018,1,5],
         'numero': 1000, 'cliente': 6, 'reserv': None}

lista_voucher = [vou_1, vou_2, vou_3, vou_4]


def date_class(lista):
    data = date(*lista)
    return data


@orm.db_session
def get_offer(num):
    offer_id = Offer[num]
    return offer_id


@orm.db_session
def add_voucher(lista_voucher):
    for voucher in lista_voucher:
        numero = voucher['numero']
        oferta_id = get_offer(voucher['oferta_id'])
        data_str = date_class(voucher['data_creation'])
        data_end = data_str + timedelta(days=365)
        reserv = voucher['reserv']
        import pdb; pdb.set_trace()
        cliente = voucher['cliente']
        Voucher(numero=numero,
                oferta=oferta_id,
                data_emizione=data_str,
                data_scadenza=data_end,
                cliente=cliente,
                )


@orm.db_session
def add_room(lista_room):
    for serv in lista_room:
        nome = serv['nome']
        descrizione = serv['descrizione']
        Room(nome=nome,
             descrizione=descrizione)


@orm.db_session
def add_offer(lista_offer):
    for serv in lista_offer:
        nome = serv['nome']
        prezzo = serv['prezzo']
        descrizione = serv['descrizione']
        Offer(nome=nome,
              prezzo=prezzo,
              descrizione=descrizione,
              )


@orm.db_session
def add_ex_serv(lista_serv):
    for serv in lista_serv:
        nome = serv['nome']
        prezzo = serv['prezzo']
        descrizione = serv['descrizione']
        Extra_services(nome=nome, prezzo=prezzo, descrizione=descrizione)


@orm.db_session
def add_guest(nome, email, telefono, altro):
    email_is = False
    try:
        email_is = Guest.select(lambda p: p.email == email)[:][0]
        email_is.email.strip()
        if email_is.id > 3801 and email_is.email != "":
            email_is.n_reservations += 1
    except:
        nome.strip()
        if ' ' in nome:
            cognome_nome = nome.split(' ')
            cognome = cognome_nome[0]
            nome = cognome_nome[1]
        else:
            cognome = ''
        email = email.strip()
        telefono = telefono.strip()
        if telefono == '' and email == '':
            pass
        else:
            Guest(nome=nome,
                  cognome=cognome,
                  email=email,
                  telefono=telefono,
                  info=altro,
                  n_reservations=0)


lista_tmp = list()
with open('model/demo_content/db.csv', 'rb') as csvfile:
    for row in csvfile:
        a = row.decode(encoding='UTF-8', errors='ignore')
        a.split(';')
        lista_tmp.append(a)

lista_end = list()
for line in lista_tmp:
    lista_end.append(str(line).split(';'))

for i in reversed(lista_end):
    try:
        nome = i[dic['nome']]
        telefono = i[dic['telefono']]
        email = i[dic['email']]
        info = i[dic['altro']]
        add_guest(nome, telefono, email, info)
    except:
        pass

add_ex_serv(lista_serv)

add_offer(lista_offer)

add_room(lista_room)

add_voucher(lista_voucher)
