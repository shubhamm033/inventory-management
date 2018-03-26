from flask_restful import Resource
from database import mongo
from flask import request,jsonify
import uuid
import hashlib
import jwt
from config import jwt_secret
from auth import auth
from flask_cors import CORS,cross_origin

class Login(Resource):
    
    @cross_origin()
    def post(self):
        
        try:
            data=request.get_json(force=True)
            
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

        try:
            if not data:
                return jsonify({"success":False,"message":"please enter details"})
        
            user_email = data.get("email").decode("utf-8")
            user_password=data.get("password").decode("utf-8")
            
            if not user_email or not user_password:

                return jsonify({"success":False,"message":"please enter proper details"})
            
            password = hashlib.sha256(user_password.encode("utf-8")).hexdigest()
            user = mongo.db.users.find_one({"email":user_email})
            
            
            if not user:
                return jsonify({"success":False,"message":"User is not registerd"})
            
            else:
                if user['password'] != password:
                    return jsonify({"success":False,"message":"incorrect password"})
            
                else:
                # f = faker.Faker()

                    token_json = {
                         #f.address() : f.sentences(),
                        "_id": user["user_id"]
                        }
                
                token =  jwt.encode(token_json, jwt_secret, algorithm="HS256")
                return jsonify({"success":True,"token": token,"username":user_email})
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})
