#!/usr/bin/env python3

from flask_session import Session
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries
from flask import Flask, jsonify, abort, request, make_response
from flask_restful import Resource, Api
import pymysql.cursors
import json

import cgitb
import cgi
import sys
import settings # Our server and db settings, stored in settings.py

api = Api(app)
cgitb.enable()

app = Flask(__name__)

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
			return make_response(jsonify({'Success': Success, 'Username': username}), 200) # turn set into json and return it

api = Api(app)
api.add_resource(SignIn, '/signin')

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "Status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "Status": "Resource not found" } ), 404)

####################################################################################
#
# Lists routing: GET and POST, individual list access
#
class Lists(Resource):
	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getLists'
			cursor = dbConnection.cursor()
			sqlArgs = (Session['username'])
			cursor.callproc(sql, sqlArgs)
			rows = cursor.fetchall()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'lists': rows}), 200)

	def post(self):
		if not request.json or not 'Name' in request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['descritpion'];
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'createList'
			cursor = dbConnection.cursor()
			sqlArgs = (Session['username'], title, description)
			cursor.callproc(sql,sqlArgs)
			row = cursor.fetchone()
			dbConnection.commit()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()

		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

####################################################################################
#
# Single list handling
#
class List(Resource):
	def get(self, listId):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getListById'
			cursor = dbConnection.cursor()
			sqlArgs = (listId)
			cursor.callproc(sql,sqlArgs)
			row = cursor.fetchone()
			if row is None:
				abort(404)
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"list": row}), 200)

	def delete(self, listId):
		print("List Id to delete: " + listId)
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteList'
			cursor = dbConnection.cursor()
			sqlArgs = (listId)
			cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return

class Items(Resource):
	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getItems'
			cursor = dbConnection.cursor()
			cursor.callproc(sql)
			rows = cursor.fetchall()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'items': rows}), 200)

	def post(self, listID):

		if not request.json or not 'Name' in request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['description'];

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'createItem'
			cursor = dbConnection.cursor()
			sqlArgs = (listID, title, description)
			cursor.callproc(sql,sqlArgs)
			row = cursor.fetchone()
			dbConnection.commit()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()

		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

class Item(Resource):
	def get(self, itemId):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getItemByID'
			cursor = dbConnection.cursor()
			sqlArgs = (itemId)
			cursor.callproc(sql,sqlArgs)
			row = cursor.fetchone()
			if row is None:
				abort(404)
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"item": row}), 200)

	def put(self, itemId):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateItem'
			title = request.json['title'];
			description = request.json['description'];
			cursor = dbConnection.cursor()
			sqlArgs = (itemId, title, description)
			cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"Item": row}), 200)

	def delete(self, itemId):
		print("Item Id to delete: " + itemId)
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteItem'
			cursor = dbConnection.cursor()
			sqlArgs = (itemId)
			cursor.callproc(sql,sqlArgs)
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/login')
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
