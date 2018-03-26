from flask_restful import Resource
from database import mongo
from flask import request,jsonify
import uuid
import hashlib
from auth import auth
from flask_cors import CORS,cross_origin 

class User(Resource):
    # @crossdomain(origin="*")
    # @auth
    # def options(self):
    #     return True
    
    @cross_origin()
    @auth
    def get(self):
        data=[]
        try:
            cursor=mongo.db.users.find({},{"_id":0})
            for user in cursor:
                data.append(user)
            return jsonify({"success":True,"response":data})

        except Exception as e:
            return jsonify({"success":False,"error":e.__str__})
    
    @cross_origin()
    # @auth
    def post(self):

        try:    
            data=request.get_json(force=True)
            print (data)

        except Exception as e:
            return jsonify({"success": False,"error":e.__str__()})

        try:
            user_email = data.get("email").decode("utf-8")
            
            if not user_email:
                return jsonify({"success":False,"message":"Please provide email"})

            user_exist=  mongo.db.users.find_one({"email":user_email})
        
            if user_exist:
                return jsonify({"success":False,"message":"User already exists"})
        
            else:
                uid = uuid.uuid4().hex
                password = hashlib.sha256(data["password"].encode("utf-8")).hexdigest()
                name=data.get("name")
                new_user={
                    "status":"Active",
                    "name":name,    
                    "email":user_email,
                    "password":password,
                    "user_id":uid
                }
                
                mongo.db.users.insert(new_user)            
                return jsonify({"success":True,"message":"user added"})
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})


class Userdelete(Resource):
    
    # @cross_origin()
    # @auth
    # def put(self):
    #     try:
            
    #         data = request.get_json(force=True)
    #         id= data["user_id"]
    #         mongo.db.categories.update({'user_id':id }, {'$set': data})
    #         return jsonify({"success":True,"message":"user updated"})
        
    #     except Exception as e:
    #         return jsonify({"success":False,"error":e.__str__()})


    
    @cross_origin()
    @auth
    def post(self):
        try:
            data=request.get_json(force=True)
            print(data)
            _id=data["id"]
            # deleted_one=mongo.db.users.find_one({"user_id":_id})
            # mongo.db.trash.insert_one(deleted_one)
            mongo.db.users.delete_one({"user_id":_id})
            return jsonify({"success":True,"message":"User deleted"})
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})
