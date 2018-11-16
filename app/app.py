#!/usr/bin/env python3

from flask_session import Session
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import json

import cgitb
import cgi
import sys
import settings

app = Flask(__name__)
api = Api(app)
cgitb.enable()

app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

@app.errorhandler(400)
def not_found(error):
	"""Handles invalid requests"""
	return make_response(jsonify( { 'Status': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	"""Handles valid requests that match no data"""
	return make_response(jsonify( { 'Status': 'Resource not found' } ), 404)

class SignIn(Resource):
	"""Handles user signin"""

	def post(self):
		"""Allows users to login, or register if they do not already exist"""
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
				dbConnection = pymysql.connect(settings.DBHOST,
					settings.DBUSER,
					settings.DBPASSWD,
					settings.DBDATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				sql = 'login'
				self.cursor = dbConnection.cursor()
				sqlArgs = (str(session['username']),)
				self.cursor.callproc(sql,sqlArgs)
				row = self.cursor.fetchone()
				dbConnection.commit()
			except LDAPException:
				response = {'Status': 'Access denied'}
				responseCode = 403
			except:
				abort(500)
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	def get(self):
		"""Valids that the user is logged in"""
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
		"""Removes the current user's session"""
		Success = False
		username = 'Not Found'
		if 'username' in session:
			Success = True
			username = session['username']
			session.clear()
		return make_response(jsonify({'Success': Success, 'Username': username}), 200)

class Users(Resource):
	"""Handles user set operations"""

	def get(self):
		"""Retrieves a list of users based on a query, default returns all users"""
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getUsers'
			self.cursor = dbConnection.cursor()
			sqlArgs = (request.args.get('user', ''), request.args.get('name', ''))
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

class User(Resource):
	"""Handles indiviual users"""

	def put(self, userId):
		"""Allows the currently logged in user to edit their information"""
		if userId != session['username']:
			abort(401)
		if not request.json:
			abort(400)
		nickname = request.json.get('nickname', '')
		description = request.json.get('description', '')
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			self.cursor = dbConnection.cursor()
			sqlArgs = (session['username'], nickname, description)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			if row is None:
				abort(404)
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({"Item": row}), 200)

	def get(self, userId):
		"""Retrieves information about a user"""
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getUserById'
			self.cursor = dbConnection.cursor()
			sqlArgs = (userId,)
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
		return make_response(jsonify({"user": row}), 200)

	def delete(self, userId):
		"""Allows a user to delete their account"""
		if userId != session['username']:
			abort(401)
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteUser'
			self.cursor = dbConnection.cursor()
			sqlArgs = (session['username'],)
			self.cursor.callproc(sql,sqlArgs)
			dbConnection.commit()
			session.clear()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({'Status': 'Removed', 'UserId': userId}), 200)

class Lists(Resource):
	"""Handles list set operations"""

	cursor = None
	dbConnection = None

	def post(self):
		""""Allows users to create new lists"""

		if 'username' not in session:
			abort(403)
		if not request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['description'];
		row = None
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

		uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

	def get(self):
		""""Allows users to retrieve lists matching a query, otherwise returns the whole set"""
		
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
			sqlArgs = (request.args.get('user', ''), request.args.get('list', ''))
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

class List(Resource):
	"""Handles indiviual lists"""

	cursor = None
	dbConnection = None

	def get(self, listId):
		"""Retrieves a list by id"""

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
			sqlArgs = (listId,)
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
		"""Deletes a list by id, if the current user is the owner"""
		if 'username' not in session:
			abort(403)
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
			sqlArgs = (session['username'], listId)
			self.cursor.callproc(sql,sqlArgs)
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({'Status': 'Removed', 'ListId': listId}), 200)

class Items(Resource):
	"""Handles item set operations"""

	cursor = None
	dbConnection = None

	def get(self):
		"""Retrieves all items associated with a list"""

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

	def post(self, listId):
		"""Adds a new item to a list"""
		if 'username' not in session:
			abort(403)
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
			sqlArgs = (listId, title, description)
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

		uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule).replace("<int:listId>", str(row['list_id']))+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( { "uri" : uri } ), 201)

class Item(Resource):
	"""Handles indiviual items"""
	cursor = None
	dbConnection = None

	def get(self, listId, itemId):
		"""Gets an item by itemId"""
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
			sqlArgs = (itemId,)
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

	def put(self, listId, itemId):
		"""Allows users to update items they own"""

		if 'username' not in session:
			abort(403)
		if not request.json:
			abort(400)
		title = request.json['title'];
		description = request.json['description'];
		try:
			dbConnection = pymysql.connect(
				settings.DBHOST,
				settings.DBUSER,
				settings.DBPASSWD,
				settings.DBDATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateItem'
			self.cursor = dbConnection.cursor()
			sqlArgs = (session['username'], itemId, title, description)
			self.cursor.callproc(sql,sqlArgs)
			row = self.cursor.fetchone()
			if row is None:
				abort(404)
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({"Item": row}), 200)

	def delete(self, listId, itemId):
		"""Allows users to deletes items they own"""

		if 'username' not in session:
			abort(403)
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
			sqlArgs = (session['username'], itemId)
			self.cursor.callproc(sql,sqlArgs)
			dbConnection.commit()
		except:
			abort(500)
		finally:
			if self.cursor is not None:
				self.cursor.close()
			if self.dbConnection is not None:
				self.dbConnection.close()
		return make_response(jsonify({'Status': 'Removed', 'ItemId': itemId}), 200)

api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:userId>')
api.add_resource(Lists, '/lists')
api.add_resource(List, '/lists/<int:listId>')
api.add_resource(Items, '/lists/<int:listId>/items')
api.add_resource(Item, '/lists/<int:listId>/items/<int:itemId>')

if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.config["PROPAGATE_EXCEPTIONS"] = True
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
