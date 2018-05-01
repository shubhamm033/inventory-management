# import pyexcel
# import os
# from flask import request,jsonify
# from flask_restful import Resource

# class Upload(Resource):
#     def post(self):
#         try:
#             # print (request.files)
#             data = request.data
#             # print(data)

#             with open("qcisaved.csv","wb") as f:
#                 f.write(data)
            
#             r = pyexcel.SeriesReader("qcisaved.csv")
#             rows=r.to_records()
            

#             # print(request.headers)
#             # # print(request.files["filename"])
#             # path = os.getcwd() + "" 
#             # filename=request.files['csv'].filename
#             # print(filename)
#             # r = pyexcel.SeriesReader(path)
#             # print(r)

#         except Exception as e:
#             return jsonify({"success":False,"error":e.__str__()})
            
        
#         header = {
                
#                 1: 'Vendor Name',
#                 2: 'Invoice No',
#                 3: 'Stock Id',
#                 4: 'Date of purchase',
#                 5: 'username',
#                 6: 'category',
#                 7: 'purchase value'
#                 }
            
        
#         for n in rows:
#             row = dict(n)
        
        


        
            



            






    

    
    

            





