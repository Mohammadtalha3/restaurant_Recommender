from app import app
from model.user_model import user_clss
import streamlit as st


from flask import request,make_response,jsonify,Response
import json
obj= user_clss()



@app.route('/store/data',methods=['POST'])
def users_show():
    yelp_data= obj.data_ingestion()
    yelp_user= obj.transfer_data_to_db(yelp_data)
    return make_response('Data Stored into Database',200)

@app.route('/show/data',methods=['GET'])
def show():
    return obj.data_ingestion()



@app.route('/restaurants/<city>/<latitude>/<longitude>',methods=['GET'])
def user_show(city,latitude,longitude):
    response= obj.search_resturant(city,latitude,longitude)

    if response:
        return(jsonify(response))
    else:
        return(jsonify({'message': 'No nearby restaurants found'}))


@app.route('/all/data', methods=['GET'])
def data_show():
    return obj.data()
    





