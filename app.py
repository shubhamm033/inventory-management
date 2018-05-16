from flask import Blueprint
from flask_restful import Api
from categories import Categories,Categoryaction
from user import User ,Userdelete
from login import Login
# from upload import Upload
from details import Details,Detailsbycategories,Deletedetail
import jwt






api_bp= Blueprint("api",__name__)
api=Api(api_bp)


api.add_resource(Categories,"/categories")
api.add_resource(Categoryaction,"/categories/deletecategory",endpoint="Categories")
api.add_resource(User,"/users")
api.add_resource(Userdelete,"/users/delete",endpoint="Users")
# api.add_resource(User,"/users",endpoint="User")
api.add_resource(Login,"/login")
api.add_resource(Details,"/details")
api.add_resource(Detailsbycategories,"/details/category",endpoint="Details")
api.add_resource(Deletedetail,"/details/delete",endpoint="DetailsDelete")
# api.add_resource(Upload,"/upload")
# api.add_resource(Useractions,"/users/action",endpoint="Users")