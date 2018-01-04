# from flask import Flask
# from flask_restful import Resource, Api
# from model.dbase import Guest
# from pony import orm

# db = orm.Database()

# db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
# orm.sql_debug(True)
# db.generate_mapping(create_tables=True)

# guest = {
# 	"nome": "Mario",
# 	"cognome": "Rossi",
# 	"nome_accompagnate": "Mayra",
# 	"cognome_accompagnate": "Perez",
# 	"email": "mario@email.com",
# 	"telefono": "45087234", 
# 	}

# class insert_guest(Resource):
# 	def get(self):
# 		@orm.db_session
# 		def insert_guest():
# 			guest = {
# 				"nome": "Mario",
# 				"cognome": "Rossi",
# 				"nome_accompagnate": "Mayra",
# 				"cognome_accompagnate": "Perez",
# 				"email": "mario@email.com",
# 				"telefono": "45087234", 
# 				}
# 			p1 = Guest(**guest)
# 			return p1.nome