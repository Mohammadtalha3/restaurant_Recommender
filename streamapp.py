import streamlit as st
import requests

st.title('Restaurant Recommender')


base_url = "http://localhost:5000"  # Replace with your Flask API base URL
restaurants_endpoint = "/restaurants/city"

selected_option = st.selectbox("Select an action:", ["","Search Restaurants"])
lat= st.text_input("Enter latitude:")
lng= st.text_input('Enter longitude:')
stat= st.selectbox('Select the state: ',
                    ("California",
                     ))
chk= st.selectbox('Please select the city: ',
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
    if lat and lng and chk and stat:
        st.button('Execute')
        full_url = f'{base_url}{restaurants_endpoint}{lat}/{lng}'
        response = requests.get(full_url,params={'city': chk})
        if response.status_code==200:
            restaurant_data= response.json()
            st.write('Restaurants Data')
            st.write(restaurant_data)
        else:
            st.error('failed to fetch data')
    else:
        st.warning('No Restaurants nearby this location')
        
            