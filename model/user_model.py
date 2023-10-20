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
        locations=['Los Angeles']

        all_locations=[]

        for location in locations:
            params={
                'term':'restaurant',
                'location':location,
                'limit':  50,
                'offset': 0
            }

           

            while True:

        

                response= requests.get(url,headers=headers,params=params)

                if response.status_code == 200:
                    data = response.json()
                    businesses = data.get('businesses', [])

                    if not businesses:
                        break

                    all_locations.extend(businesses)

                    if 'pagination' in data and 'next_offset' in data['pagination']:
                        params['offset'] = data['pagination']['next_offset']
                    else:
                        break  # No more pages


                

                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    break

            return all_locations
        


    def transfer_data_to_db(self, data):
        if data:
            for business in data:
                # Insert business data into the database
                insert_query = """
                INSERT IGNORE INTO businesses (
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
                    print(f"Error inserting data into the businesses table: {err}")

                # Insert category data into the database
                categories = business.get('categories', [])
                for category in categories:
                    category_alias = category.get('alias', '')
                    category_title = category.get('title', '')

                    category_insert_query = """
                    INSERT INTO categories (business_id, alias, title) VALUES (%s, %s, %s)
                    """
                    category_values = (business['id'], category_alias, category_title)

                    try:
                        self.mycursor.execute(category_insert_query, category_values)
                    except mysql.connector.Error as err:
                        print(f"Error inserting data into the categories table: {err}")

                # Insert location data into the database
                location = business.get('location', {})
                loc_address1 = location.get('address1', '')
                loc_address2 = location.get('address2', '')
                loc_address3 = location.get('address3', '')
                loc_city = location.get('city', '')
                loc_country = location.get('country', '')
                loc_zip = location.get('zip_code', '')
                loc_state = location.get('state', '')

                location_insert_query = """
                INSERT INTO locations (business_id, address1, address2, address3, city, country, zip_code, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                location_values = (
                    business['id'], loc_address1, loc_address2, loc_address3,
                    loc_city, loc_country, loc_zip, loc_state
                )

                try:
                    self.mycursor.execute(location_insert_query, location_values)
                except mysql.connector.Error as err:
                    print(f"Error inserting data into the locations table: {err}")

            # Commit the changes to the database
           
        else:
            print("No data to transfer to the database")

    def search_resturant(self,city,latitude,longitude):
            if not (city and latitude and longitude) :
                return make_response('Latitude and longitude are required for recommendations.',400)
        

            query="""SELECT b.name AS resturant_name,
                b.id,
                b.is_closed,
                b.review_count,
                b.rating,
                b.display_phone,
                b.distance,
                l.address1,
                l.address2
                
                FROM 
                    businesses AS b
                INNER JOIN 
                    locations AS l ON b.id=l.business_id
               WHERE 
                    l.city = %s
                ORDER BY 
                    SQRT(POW(b.latitude - %s, 2) + POW(b.longitude - %s, 2)) ASC
                """
            
          
        
            self.mycursor.execute(query, (city,latitude,longitude))
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



    

    
    def data(self):
        query='SELECT DISTINCT state from locations '

        self.mycursor.execute(query)
        returants= self.mycursor.fetchall()

        unique_cities=set()

        for cit in returants:
            unique_cities.add(cit['city'])

            unique_cities_list = list(unique_cities)

        return unique_cities_list


       



    


    