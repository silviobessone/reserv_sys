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

dic = {'nome': 2,  'telefono': 5, 'email': 4, 'altro': 17}


class Guest(db.Entity):
    nome = orm.Optional(str)
    cognome = orm.Optional(str)
    email = orm.Optional(str)
    telefono = orm.Optional(str)
    info = orm.Optional(str)
    n_reservations = orm.Optional(int)

db.bind(provider='sqlite', filename='raw_database.sqlite', create_db=True)
orm.sql_debug(False)
db.generate_mapping(create_tables=True)


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
with open('db.csv', 'rb') as csvfile:
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
