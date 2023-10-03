from app import app
from model.user_model import user_clss


from flask import request,make_response,jsonify,Response
import json
obj= user_clss()



@app.route('/store/businesses',methods=['POST'])
def users_show():
    yelp_data= obj.data_ingestion()
    yelp_user= obj.transfer_data_to_db(yelp_data)
    return make_response('Data Stored into Database',200)

@app.route('/store/categories',methods=['POST'])
def user_categories():
    yelp_data= obj.data_ingestion()
    yelp_user= obj.transfer_data_cat(yelp_data)
    return make_response('categories transfered',200)

@app.route('/store/location',methods=['POST'])
def user_lcoation():
    yelp_data=obj.data_ingestion()
    obj.location_transfer(yelp_data)
    return make_response('Location transfered succesfully',200)


@app.route('/resturants/<location>',methods=['GET'])
def user_show(location):
    return jsonify(obj.search_resturant(location))



