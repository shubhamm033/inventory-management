from flask_restful import Resource
from flask import request,jsonify
from database import mongo
from auth import auth
import uuid

from flask_cors import CORS,cross_origin
from general import *


class Categories(Resource):
    
    @cross_origin()
    @auth
    def get(self):
        data=[]
        try:
            cursor = mongo.db.categories.find({}, {"_id": 0})
            for category in cursor:
                if "last_updated" in category:
                    category["last_edited"] = nicetime(category["last_updated"])                    
                else:
                    category["last_edited"] = ""
                    category["last_updated"] = 100**10                
                data.append(category)
            
            data = sorted(data,key=lambda i:i["last_updated"],reverse=True)
            return jsonify({"success":True,"response": data})
       
        except Exception as e:
           return jsonify({"success": False,"error" : e.__str__() })            


    @cross_origin()
    @auth
    def post(self):
        
            try: 
                
                data = request.get_json(force=True)
                
            except Exception as e:
                return jsonify({"success": False,"message": "No data provided","error" : e.__str__() })    
                

            category = data.get('category')
            category_exist=mongo.db.categories.find_one({"category": category})

            try:    
                if category_exist:
                    return jsonify({"success": False,"message": "Category already exists"})
                
                else:
                    uid = uuid.uuid4().hex
                    new_category={
                        "category":category,
                        "category_id":uid,
                        "status":"Active",
                         "created_at":itime(),
                         "last_updated":itime()
                        }
                    mongo.db.categories.insert_one(new_category)
                    return jsonify({"success":True,"message":"Category added","category_id":uid})
            
            except Exception as e:
                return jsonify({"success": False,"error" : e.__str__() })
            


class Categoryaction(Resource):


    
    
    @cross_origin()
    @auth
    def post(self):
        try:
            data=request.get_json(force=True)
            
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})
            
        try:    
            category_id=data["category_id"]
            details_exist_from_category=mongo.db.details.find_one({"category_id":category_id})
            
            if details_exist_from_category:
                return jsonify({"success":False,"message":"Category can't be deleted"})
            
            
            else:
                mongo.db.categories.remove({"category_id":category_id})
                return jsonify({"success":True,"message":"Category deleted"})            
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

        
    


