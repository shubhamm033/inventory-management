import os
basedir = os.path.abspath(os.path.dirname(__file__))
jwt_secret="mykey"

# class Config(object):
#     DEBUG = False
#     # MONGO_URI = 'mongodb://localhost:27017/mydb'
#     MONGO_URI = os.getenv('MONGO_URL')
# class DevelopmentConfig(Config):

#         DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False


# app_config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig
# }    

# #     # Database
# #     MONGO_URI = 'mongodb://localhost:27017/mydb'
# #     # MONGO_USERNAME = 'mydb'
# #     # MONGO_PASSWORD = 'password'

# #     # Debugging
# #     DEBUG = False

#     # Networking
#     # PORT = 5000
    # PREFERRED_URL_SCHEME = 'https'
    # SERVER_NAME = 'mywebsite.com'
