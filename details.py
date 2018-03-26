from flask_restful import Resource
from flask import request,jsonify
from database import mongo
from auth import auth 
import uuid
from flask_cors import CORS,cross_origin
import datetime
import json

from general import *

class Details(Resource):

    
    @cross_origin()
    @auth
    def get(self):
        data=[]
        
        try:
            cursor=mongo.db.details.find({},{"_id": 0})
            for detail in cursor:
                
                data.append(detail)       
            return jsonify({"success":True,"response":data}) 
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})
    
    
    
    
    @cross_origin()
    @auth
    def post(self):
        
        try:
            data=request.get_json(force=True)
            print(data)
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__})
        
        try:
            if data["details_id"]!="":
                _id = data["category_id"]
                set_details={
                    "stock_id":data["stock_id"],
                    "purchase_value":data["purchase_value"],
                    "vendor_name":data["vendor_name"],
                    "location":data["location"],
                    "invoice_no":data["invoice_no"],
                    "date_of_purchase":dateToepoch(data["date_of_purchase"]),
                    "last_updated":itime()
                }
                mongo.db.details.update_one({'details_id':data["details_id"] },{"$set":set_details})
                mongo.db.categories.update_one({'category_id':_id },{"$set":{"last_updated":itime()}})
            else:
                uid = uuid.uuid4().hex
                _id = data["category_id"]
                new_detail={"details_id":uid,
                            "stock_id":data["stock_id"],
                            "purchase_value":data["purchase_value"],
                            "vendor_name":data["vendor_name"],
                            "location":data["location"],
                            "invoice_no":data["invoice_no"],
                            "date_of_purchase":dateToepoch(data["date_of_purchase"]),
                            "created_at":itime(),
                            "last_updated":itime(),
                            "category_id": _id
                }
                mongo.db.details.insert(new_detail)
                
                mongo.db.categories.update_one({'category_id':_id },{"$set":{"last_updated":itime()}})
            return jsonify({"success":True, "message": "new_details added" })
    
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})



    
    
    

class Detailsbycategories(Resource):
    
    @cross_origin()
    @auth
    def post(self):
        details_list=[]
        
        try:
            # print (request.data)
            # print (request.args)
            # print (json.loads(request.values))            

            data=request.get_json(force=True)
            print (data)
        
        except Exception as e:
            return jsonify({"response":False,"error":e.__str__()})

            
        category_id=data["id"]
        
        try:
            if category_id:
                print (category_id)
                cursor=mongo.db.details.find({"category_id":category_id},{"_id": 0})
                for detail in cursor:
                    
                    if "last_updated" in detail:
                        detail["last_updated"] = nicetime(detail["last_updated"])
                    if "date_of_purchase" in detail:
                        detail["date_of_purchase"] = nicetime(detail["date_of_purchase"])    
                    details_list.append(detail)
                return jsonify({"success":True,"response":details_list})
            
            else:
                return jsonify({"success":False,"response":"No category provided"})
        
        except Exception as e:
            return jsonify({"response":False,"error":e.__str__()})
            
class Deletedetail(Resource):
    @cross_origin()
    @auth
    def post(self):
        try:
            data=request.get_json(force=True)
            print (data)
            _id=data["details_id"]
            deleted_one=mongo.db.details.find_one({"details_id":_id})
            mongo.db.trash.insert_one(deleted_one)
            mongo.db.details.delete_one({"details_id":_id})
            return jsonify({"success":True,"message":"inventory detail deleted"})
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})


    