
from flask_pymongo import MongoClient
mongo_ip = "172-31-28-161"
# mongo_ip = "localhost"
mongo_port = 27017
uri  = "mongodb://" + mongo_ip + ":" + str(mongo_port)+"/"
mongo = MongoClient(uri)
