import streamlit as st
from controller.user_controller import user_show
import requests

st.title('Restaurant Recommender')


base_url = "http://localhost:5000"  # Replace with your Flask API base URL
restaurants_endpoint = "/restaurants"

selected_option = st.selectbox("Select an action:", ["","Search Restaurants"])
lat= st.text_input("Enter latitude:")
lng= st.text_input('Enter longitude:')
'''stat= st.selectbox('Select the state: ',
                    ("California",
                     "West Hollywood"
                     ))'''
city= st.selectbox('Please select the city: ',
                  ( "Mammoth Lakes",
                    "Los Angeles",
                    "Midpines",
                    "Groveland",
                    "El Portal",
                    "Coarsegold",
                    "Badger",
                    "North Fork",
                    "Shaver Lake",
                    "Catheys Valley",
                    "Dunlap",
                    "Oakhurst",
                    "June Lake",
                    "West Hollywood",
                    "Fish Camp",
                    "Miramonte",
                    "Auberry",
                    "Prather",
                    "San Francisco",
                    "Bass Lake",
                    "Tollhouse",
                    "Mariposa",
                    "Bishop",
                    "North Hollywood"))

if selected_option=='Search Restaurants':
    st.button('Execute')
    if lat and lng and city :
        
        full_url = f'{base_url}{restaurants_endpoint}/{city}/{lat}/{lng}'
        response = requests.get(full_url)
        if response.status_code==200:
            restaurant_data= response.json()
            st.write('Restaurants Data')
            st.write(restaurant_data)
        else:
            st.error('failed to fetch data')
    else:
        st.warning('No Restaurants nearby this location')
        
            