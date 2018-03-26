from flask import Flask
from flask_cors import CORS
import flask_excel

# from config import app_config



def create_app(config_filename):
    app=Flask(__name__)
    CORS(app,support_credentials=True)
    app.config["CORS_HEADERS"]='Authorization'


    
    
    app.config.from_object(config_filename)
    from app import api_bp
    app.register_blueprint(api_bp,url_prefix="/inventory")

    # flask_excel.init_excel(app)
    # print(flask_excel)
    
    return app

if __name__== "__main__":
    app=create_app("config")
    app.run(host="0.0.0.0",debug=True)