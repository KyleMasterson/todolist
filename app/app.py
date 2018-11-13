#!/usr/bin/env python3

from flask_session import Session
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import json

import cgitb
import cgi
import sys
import settings # Our server and db settings, stored in settings.py

app = Flask(__name__)
api = Api(app)
cgitb.enable()

# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'Status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'Status': 'Resource not found' } ), 404)

class SignIn(Resource):
	def post(self):
		if not request.json:
			abort(400)

		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)

		if request_params['username'] in session:
			response = {'Status': 'Success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				session['username'] = request_params['username']
				response = {'Status': 'Success' }
				responseCode = 201
			except LDAPException:
				response = {'Status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	def get(self):
		Success = False
		if 'username' in session:
			username = session['username']
			response = {'Status': 'Success'}
			responseCode = 200
		else:
			response = {'Status': 'Fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	def delete(self):
			Success = False
			username = 'Not Found'
			if 'username' in session:
				Success = True
				username = session['username']
				session.clear()
			return make_response(jsonify({'Success': Success, 'Username': username}), 200)

####################################################################################
#
# Lists routing: GET and POST, individual list access
#
class Lists(Resource):

	cursor = None
	dbConnection = None

	def post(self):
		if not request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['description'];
		try:
			dbConnection = pymysql.connect(settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'createList'
			self.cursor = dbConnection.cursor()
			sqlArgs = (session['username'], title, description)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()

		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getLists'
			self.cursor = dbConnection.cursor()
			sqlArgs = (session['username'])
			self.cursor.callproc(sql, sqlArgs)
			rows = self.cursor.fetchall()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({'lists': rows}), 200)

####################################################################################
#
# Single list handling
#
class List(Resource):

	cursor = None
	dbConnection = None

	def get(self, listId):
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getListById'
			self.cursor = dbConnection.cursor()
			sqlArgs = (listId)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			if row is None:
				abort(404)
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({"list": row}), 200)

	def delete(self, listId):
		print("List Id to delete: " + listId)
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteList'
			self.cursor = dbConnection.cursor()
			sqlArgs = (listId)
			self.cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return

class Items(Resource):

	cursor = None
	dbConnection = None

	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getItems'
			self.cursor = dbConnection.cursor()
			self.cursor.callproc(sql)
			rows = self.cursor.fetchall()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({'items': rows}), 200)

	def post(self, listID):

		if not request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['description'];

		try:
			dbConnection = pymysql.connect(settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'createItem'
			self.cursor = dbConnection.cursor()
			sqlArgs = (listID, title, description)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()

		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

class Item(Resource):

	cursor = None
	dbConnection = None

	def get(self, itemId):
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getItemByID'
			self.cursor = dbConnection.cursor()
			sqlArgs = (itemId)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			if row is None:
				abort(404)
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({"item": row}), 200)

	def put(self, itemId):
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateItem'
			title = request.json['title'];
			description = request.json['description'];
			self.cursor = dbConnection.cursor()
			sqlArgs = (itemId, title, description)
			self.cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({"Item": row}), 200)

	def delete(self, itemId):
		print("Item Id to delete: " + itemId)
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteItem'
			self.cursor = dbConnection.cursor()
			sqlArgs = (itemId)
			self.cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(Lists, '/lists')
api.add_resource(List, '/lists/<int:listId>')
api.add_resource(Items, '/lists/<int:listId>/Items')
api.add_resource(Item, '/lists/<int:listId>/Items/<int:itemId>')

#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.config["PROPAGATE_EXCEPTIONS"] = True
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
