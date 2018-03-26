import pyexcel
import os
from flask import request,jsonify
from flask_restful import Resource

class Upload(Resource):
    def post(self):
        try:
            file = request.files
            file['file']


            
            # print(request.headers)
            # # print(request.files["filename"])
            # path = os.getcwd() + "" 
            # filename=request.files['csv'].filename
            # print(filename)
            # r = pyexcel.SeriesReader(path)
            # print(r)

        
            
            # rows = r.to_records()

            
            return jsonify({"result": "yes"})
        
        
        except Exception as e:
                return({"success":False,"error":e.__str__()})



            






    

    
    

            





