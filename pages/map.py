import streamlit as st
import folium
from streamlit_folium import st_folium

import asyncio
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

st.set_page_config(page_title="Compost @ UVA", layout="wide")
st.title("Compost Bin Locations at UVA")

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

st.sidebar.page_link('pages/leaderboard.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

bins = [
  { "name": "West Range Café", "lat": 38.03440597950913, "lng": -78.50549149999998 }, # 38.03440597950913, -78.50549149999998
  { "name": "Fine Arts Café", "lat": 38.038935874378204, "lng": -78.50381527116451 }, # 38.038935874378204, -78.50381527116451
  { "name": "McIntire Amphitheater", "lat": 38.03375558244706, "lng": -78.50571341349354 }, # 38.03375558244706, -78.50571341349354
  { "name": "Observatory Hill", "lat": 38.034942731019754, "lng": -78.51516124232904 }, # 38.034942731019754, -78.51516124232904
  { "name": "International Residence College", "lat": 38.03952102315012, "lng": -78.50730390610003 }, # 38.03952102315012, -78.50730390610003
  { "name": "Hereford College", "lat": 38.03083695052635, "lng": -78.5186306269871 }, # 38.03083695052635, -78.5186306269871
  { "name": "Brown College", "lat": 38.03486438244903, "lng": -78.50744853308716 }, # 38.03486438244903, -78.50744853308716
  { "name": "The Lawn", "lat": 38.0354069820986, "lng": -78.50327330610004 }, # 38.0354069820986, -78.50327330610004
  { "name": "McIntire Recycling Center", "lat": 38.0378672261271, "lng": -78.47939726561937 }, # 38.0378672261271, -78.47939726561937
  { "name": "Charlottesville City Market", "lat": 38.02977369272681, "lng": -78.48148841349354, "notes": "Drop-off location available April through October" } # 38.02977369272681, -78.48148841349354
]

m=folium.Map(location=[38.0336, -78.5080], zoom_start=14)

 
for bin in bins:
    popup = f"""
    <b>{bin['name']}</b><br>
    """
    if "notes" in bin:
        popup += f"{bin['notes']}"
    
    folium.Marker(
        location=[bin["lat"], bin["lng"]],
        popup=popup,
        icon=folium.Icon(color="green", icon="leaf", prefix="fa")
    ).add_to(m)  

st_data = st_folium(m, width=800, height=600)
