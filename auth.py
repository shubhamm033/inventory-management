from flask import request,jsonify
from config import jwt_secret
from functools import wraps
from config import jwt_secret
import jwt
#from general import * 
def auth(func):
		@wraps(func) # to preserve name, docstring, etc.
		def decorated(*args, **kwargs):
			try:
				token = request.headers["Authorization"]
				# print(token)	
				_id = jwt.decode(token, jwt_secret, algorithms=["HS256"])["_id"]
			except Exception as e:
				return jsonify({"response" : 'Headers required'})
			return func( *args, **kwargs)
		return decorated