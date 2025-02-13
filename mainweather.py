import streamlit as st
import requests
import os

# Function to fetch weather data
def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY", "3c1d901aba98438bacb44730251302")  # Store API key in an environment variable
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise HTTP errors if any
        data = response.json()

        if "error" in data:
            return None, data["error"]["message"]

        weather_info = {
            "City": data["location"]["name"],
            "Country": data["location"]["country"],
            "Temperature": f"{data['current']['temp_c']}°C",
            "Feels Like": f"{data['current']['feelslike_c']}°C",
            "Humidity": f"{data['current']['humidity']}%",
            "Pressure": f"{data['current']['pressure_mb']} hPa",
            "Wind Speed": f"{data['current']['wind_kph']} kph",
            "Condition": data["current"]["condition"]["text"],
            "Icon": data["current"]["condition"]["icon"],
            "UV Index": data["current"]["uv"],
            "Visibility": f"{data['current']['vis_km']} km"
        }

        return weather_info, None

    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {e}"

# Streamlit UI
st.title("🌤 Real-Time Weather App")
st.write("Enter a city name to get up-to-date weather information.")

city_name = st.text_input("City Name", "Mumbai")

if st.button("Get Weather"):
    weather, error = get_weather(city_name)

    if error:
        st.error(f"Error: {error}")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"Weather in {weather['City']}, {weather['Country']}")
            st.write(f"*Condition:* {weather['Condition']}")

        with col2:
            st.image(f"http:{weather['Icon']}", width=80)

        st.metric("🌡 Temperature", weather["Temperature"])
        st.metric("🤒 Feels Like", weather["Feels Like"])
        st.metric("💧 Humidity", weather["Humidity"])
        st.metric("🌬 Wind Speed", weather["Wind Speed"])
        st.metric("🔵 Pressure", weather["Pressure"])
        st.metric("☀ UV Index", weather["UV Index"])
        st.metric("👀 Visibility", weather["Visibility"])
