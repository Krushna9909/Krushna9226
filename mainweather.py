import streamlit as st
import requests

# OpenWeatherMap API key
api_key = '8fd7660b97d4222400bbf2f8209c3311'

# Function to get weather data
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()

# Streamlit app
st.title("Weather App")
city = st.text_input("Enter city name", "New York")

if st.button("Get Weather"):
    data = get_weather(city)
    if data["cod"] != "404":
        main = data["main"]
        wind = data["wind"]
        weather = data["weather"][0]
        
        st.write(f"**Temperature:** {main['temp']} K")
        st.write(f"**Pressure:** {main['pressure']} hPa")
        st.write(f"**Humidity:** {main['humidity']}%")
        st.write(f"**Weather:** {weather['description']}")
        st.write(f"**Wind Speed:** {wind['speed']} m/s")
    else:
        st.error("City Not Found!")
