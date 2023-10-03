import requests
import mysql.connector
import sys
import pandas as pd
from flask import Flask, make_response




class user_clss():

    def __init__(self):
        try:
            self.conn= mysql.connector.connect(host='localhost',user='root',password='mysql',database='yelp')
            self.conn.autocommit=True
            self.mycursor= self.conn.cursor(dictionary=True)
        except:
            print("Couldn't connect to database")
        else:
            print('Conencted to database')


    def data_ingestion(self):
        url="https://api.yelp.com/v3/businesses/search"
        api_key='kmAtvzMtovEgIMoCnkJIOaH7fI8VAmzel_mMp7kCumtNEvFoDhyITeqdhGPIiKu3doud5RhPefBPk5MA49QkR2VmTyENv-wkXLwtQz-fsT3kzzliPFLNuXHzm50CZXYx'
        headers={
            'Authorization': f'Bearer {api_key}' }
        params={
                'term':'restaurant',
                'location':'San Francisco'
        }
        

        dt= requests.get(url,headers=headers,params=params)
        



        if dt.status_code==200:
            dt2= dt.json()
            return dt2
            
        else:            
            print(f"message:{'Operation could not complete'}")
    
    def transfer_data_to_db(self, data):
        if data:
            # Iterate through businesses in the data and insert them into the database
            for business in data.get('businesses', []):
                insert_query = """
                INSERT INTO businesses (
                    id, alias, name, image_url, is_closed, url, review_count, rating,
                    latitude, longitude, phone, display_phone, distance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    business['id'],
                    business['alias'],
                    business['name'],
                    business['image_url'],
                    business['is_closed'],
                    business['url'],
                    business['review_count'],
                    business['rating'],
                    business['coordinates']['latitude'],
                    business['coordinates']['longitude'],
                    business['phone'],
                    business['display_phone'],
                    business['distance'],
                )

                try:
                    self.mycursor.execute(insert_query, values)
                except mysql.connector.Error as err:
                    print(f"Error inserting data into the database: {err}")
        else:
            print("No data to transfer to the database")
    
    def transfer_data_cat(self,data):
        if data:
            for business in data.get('businesses',[]):
                valid_id= business.get('id','')
                categories= business.get('categories',[])

                for category in categories:
                    category_alias= category.get('alias','')
                    category_title= category.get('title','')
                Insert_query="""INSERT INTO  categories(business_id,alias,title) VALUES(%s,%s,%s)"""
                

                values=(valid_id,category_alias,category_title)

                try:
                    self.mycursor.execute(Insert_query,values)
                except mysql.connector.Error as err:
                    print(f"Error inserting into database:  {err}")
        else:
            print('No data to transfer to the database')
    
    def location_transfer(self,data):
        if 'businesses' in  data:
            for business in data.get('businesses',[]):
                valid_id=business.get('id','')
                location= business.get('location',{})
                display_address=business.get('display_address',[])

                
                loc_address1= location.get('address1','')
                loc_address2= location.get('address2','')
                loc_address3= location.get('address3','')
                loc_city= location.get('city','')
                loc_country= location.get('country','')
                loc_zip= location.get('zip_code','')
                loc_state= location.get('state','')
                insert_query= """INSERT INTO  locations(business_id,address1,address2,address3,city,country,zip_code,state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""

                values=(valid_id,loc_address1,loc_address2,loc_address3,loc_city,loc_country,loc_zip,loc_state)

                try:
                    self.mycursor.execute(insert_query,values)
                except mysql.connector.Error as err:
                    print(f"Error inserting to database: {err}")
        else:
            print('No data to transfer to the database')
    

    def search_resturant(self,location):
        if not location:
            return make_response('No resturant found',400)
        

        query="""SELECT b.name AS resturant_name, b.is_closed,b.review_count,b.rating,b.display_phone,b.distance,l.address1,l.address2
                 FROM businesses AS b
                 INNER JOIN locations AS l ON b.id=l.business_id
                 WHERE city=%s
                """
        
        self.mycursor.execute(query, (location,))
        resturants= self.mycursor.fetchall()

        response=[]
        for d in resturants:
            location_info={
                'Address1': d['address1'],
                'Address2': d['address2'],
                'distance': d['distance']

            }
            status={
                'open': d['is_closed'],
                'review': d['review_count'],
                'rating': d['rating'],
                'contact': d['display_phone'],

            }

            response.append({
                'Restaurant name': d['resturant_name'],
                'Status':status,
                'Locations': location_info,


            })

            return response
       



    


    