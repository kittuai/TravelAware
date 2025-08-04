import streamlit as st
import pandas as pd
import folium
import random
from datetime import datetime, timedelta
from folium.plugins import HeatMap, MarkerCluster
from shapely.geometry import Point, Polygon
from streamlit_folium import st_folium

# ----------------- Page Setup -----------------
st.set_page_config("TravelAware", layout="wide")
st.title("🛡️ TravelAware – Real-Time Safety Assistant")

# ----------------- User Location -----------------
if "user_location" not in st.session_state:
    st.session_state.user_location = (43.4643, -80.5204)  # Waterloo fallback

user_lat, user_lon = st.session_state.user_location
st.sidebar.success(f"📍 Location: {user_lat:.4f}, {user_lon:.4f}")

# ----------------- Define Zones -----------------
zones = [
    Polygon([(43.459, -80.540), (43.461, -80.538), (43.460, -80.536), (43.458, -80.537)]),
    Polygon([(43.470, -80.515), (43.472, -80.513), (43.471, -80.511), (43.469, -80.512)]),
    Polygon([(43.476, -80.500), (43.478, -80.498), (43.477, -80.496), (43.475, -80.497)]),
    Polygon([(43.455, -80.530), (43.457, -80.528), (43.456, -80.526), (43.454, -80.527)]),
    Polygon([(43.466, -80.525), (43.468, -80.523), (43.467, -80.521), (43.465, -80.522)]),
    Polygon([(43.462, -80.508), (43.464, -80.506), (43.463, -80.504), (43.461, -80.505)]),
    Polygon([(43.473, -80.534), (43.475, -80.532), (43.474, -80.530), (43.472, -80.531)]),
    Polygon([(43.450, -80.520), (43.452, -80.518), (43.451, -80.516), (43.449, -80.517)])
]

# ----------------- Generate Crimes -----------------
def generate_crimes():
    crimes = []
    now = datetime.now()
    for idx, zone in enumerate(zones):
        minx, miny, maxx, maxy = zone.bounds
        for _ in range(random.randint(4, 8)):
            while True:
                lat = random.uniform(minx - 0.0025, maxx + 0.0025)
                lon = random.uniform(miny - 0.0025, maxy + 0.0025)
                if random.random() < 0.75 and not zone.contains(Point(lat, lon)):
                    continue
                crimes.append({
                    "lat": lat,
                    "lon": lon,
                    "type": random.choice(["Assault", "Theft", "Robbery", "Break & Enter"]),
                    "date": now - timedelta(hours=random.randint(1, 72)),
                    "zone": idx
                })
                break
    return pd.DataFrame(crimes)

if "crimes_df" not in st.session_state:
    st.session_state.crimes_df = generate_crimes()

df = st.session_state.crimes_df

# ----------------- Banner: Recent Crime Count -----------------
last_24h = df[df['date'] > datetime.now() - timedelta(hours=24)]
st.markdown(f"### 📢 In the last 24 hours, **{len(last_24h)}** crimes were reported near you.")

# ----------------- Sidebar -----------------
st.sidebar.markdown("## 🔘 Quick Actions")

with st.sidebar.expander("🚶 Safe Route Suggestion"):
    from_street = st.text_input("From:")
    to_street = st.text_input("To:")
    if st.button("Suggest Safe Route"):
        st.info(f"🧭 Avoid **{from_street}**, take **{to_street}** instead, and stick to major well-lit streets. Avoid alleys and isolated areas.")

if st.sidebar.button("📝 Report a Crime"):
    st.session_state.show_form = True

if st.sidebar.button("📰 Crime Feed"):
    st.session_state.show_feed = True

if st.sidebar.button("🚨 Send SOS"):
    st.sidebar.error("🆘 SOS sent to emergency contacts! (Simulated)")

# ----------------- Map Toggle -----------------
map_type = st.radio("🗺️ Map View", ["Heatmap", "Cluster"], horizontal=True)

# ----------------- Map Setup -----------------
m = folium.Map(location=[user_lat, user_lon], zoom_start=13)
folium.Marker([user_lat, user_lon], popup="📍 You are here", icon=folium.Icon(color="blue")).add_to(m)

if map_type == "Heatmap":
    HeatMap(
        df[["lat", "lon"]].values.tolist(),
        radius=16, blur=18, min_opacity=0.4,
        gradient={0.2: 'yellow', 0.5: 'orange', 0.8: 'red'}
    ).add_to(m)
else:
    cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=f"<b>{row['type']}</b><br>{row['date'].strftime('%b %d, %Y %I:%M %p')}",
            icon=folium.Icon(color="red")
        ).add_to(cluster)
    for zone in zones:
        folium.Polygon(
            locations=[(lat, lon) for lat, lon in zone.exterior.coords],
            color="crimson", fill=True, fill_opacity=0.28,
            tooltip="⚠️ High-Risk Zone"
        ).add_to(m)

# ----------------- Map Interaction -----------------
result = st_folium(m, width=1100, height=600)

if result and result.get("last_clicked"):
    lat = result["last_clicked"]["lat"]
    lon = result["last_clicked"]["lng"]
    clicked_point = Point(lat, lon)
    inside = any(zone.contains(clicked_point) for zone in zones)
    if inside:
        st.warning("🚨 You entered a **high-risk neighborhood zone**.")
    else:
        st.info("✅ This appears to be a **low-risk area**.")

# ----------------- Report Form -----------------
if st.session_state.get("show_form"):
    st.subheader("📢 Report a Crime")
    with st.form("report_form"):
        crime_type = st.selectbox("Crime Type", ["Assault", "Theft", "Robbery", "Break & Enter"])
        desc = st.text_area("Description (optional)")
        crime_time = st.time_input("Time occurred:")
        submit = st.form_submit_button("Submit Report")
        if submit:
            urgency = random.choice(["Low", "Medium", "High"])
            eta = random.randint(7, 28)
            st.success("✅ Report submitted (simulated).")
            st.info(f"🧨 Predicted Urgency: **{urgency}**")
            st.info(f"🚓 Estimated Response Time: **{eta} minutes**")
            st.session_state.show_form = False

# ----------------- Crime Feed -----------------
if st.session_state.get("show_feed"):
    st.subheader("📰 Recent Crime Feed")
    for _, row in df.sort_values("date", ascending=False).head(8).iterrows():
        st.markdown(f"**{row['type']}** – *{row['date'].strftime('%b %d, %Y %I:%M %p')}*")
        st.caption(f"Zone {row['zone']} | Location: ({row['lat']:.4f}, {row['lon']:.4f})")
        st.markdown("---")
    st.session_state.show_feed = False

# ----------------- Footer -----------------
