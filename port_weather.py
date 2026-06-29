import csv
import requests
import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Port Weather Checker",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp {
        background-color: #06101C;
        color: #E8EDF2;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }

    .hero-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        border-bottom: 1px solid #1E3A5F;
        margin-bottom: 2rem;
    }
    .hero-anchor {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem;
        letter-spacing: 0.06em;
        color: #F59E0B;
        line-height: 1;
        margin: 0;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3rem;
        letter-spacing: 0.12em;
        color: #FFFFFF;
        line-height: 1;
        margin: 0 0 0.5rem 0;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #7A9BBF;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.04em;
    }

    .search-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #F59E0B;
        margin-bottom: 0.4rem;
    }

    .stTextInput > div > div > input {
        background-color: #0D1E30 !important;
        border: 1.5px solid #1E3A5F !important;
        border-radius: 8px !important;
        color: #E8EDF2 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #F59E0B !important;
        box-shadow: 0 0 0 2px rgba(245,158,11,0.25) !important;
    }
    .stSelectbox > div > div {
        background-color: #0D1E30 !important;
        border: 1.5px solid #1E3A5F !important;
        border-radius: 8px !important;
        color: #E8EDF2 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #0D1E30 !important;
        border-color: #1E3A5F !important;
        color: #E8EDF2 !important;
    }

    .stButton > button {
        background-color: #F59E0B !important;
        color: #06101C !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 2.5rem !important;
        width: 100% !important;
        transition: background 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #FBBF24 !important;
    }

    .section-card {
        background-color: #0D1E30;
        border: 1px solid #1E3A5F;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
    }
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #F59E0B;
        margin: 0 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #1E3A5F;
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: 0.35rem 0;
        border-bottom: 1px solid #0F2540;
    }
    .stat-row:last-child { border-bottom: none; }
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #7A9BBF;
        font-weight: 500;
    }
    .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        font-weight: 600;
        color: #E8EDF2;
        text-align: right;
    }
    .stat-value.green  { color: #34D399; }
    .stat-value.amber  { color: #F59E0B; }
    .stat-value.orange { color: #FB923C; }
    .stat-value.red    { color: #F87171; }

    .verdict-safe {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 100%);
        border: 1.5px solid #34D399;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-bottom: 1.4rem;
    }
    .verdict-warning {
        background: linear-gradient(135deg, #78350F 0%, #92400E 100%);
        border: 1.5px solid #F59E0B;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-bottom: 1.4rem;
    }
    .verdict-critical {
        background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 100%);
        border: 1.5px solid #F87171;
        border-radius: 14px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-bottom: 1.4rem;
    }
    .verdict-icon {
        font-size: 3rem;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .verdict-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.2rem;
        letter-spacing: 0.1em;
        margin: 0;
    }
    .verdict-title.safe     { color: #34D399; }
    .verdict-title.warning  { color: #F59E0B; }
    .verdict-title.critical { color: #F87171; }
    .verdict-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #CBD5E1;
        margin: 0.3rem 0 0 0;
    }

    .alert-pill {
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.6rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }
    .alert-pill.critical {
        background-color: rgba(248,113,113,0.12);
        border-left: 3px solid #F87171;
        color: #FCA5A5;
    }
    .alert-pill.warning {
        background-color: rgba(245,158,11,0.12);
        border-left: 3px solid #F59E0B;
        color: #FCD34D;
    }
    .alert-pill.advisory {
        background-color: rgba(96,165,250,0.10);
        border-left: 3px solid #60A5FA;
        color: #93C5FD;
    }
    .alert-badge {
        font-weight: 700;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        white-space: nowrap;
        padding-top: 0.05rem;
    }

    .port-name-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.4rem;
        letter-spacing: 0.08em;
        color: #FFFFFF;
        margin: 0 0 0.15rem 0;
    }
    .port-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #4A7098;
        margin: 0;
    }

    hr { border-color: #1E3A5F; margin: 1.5rem 0; }

    .no-results {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #4A7098;
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_ports():
    csv_path = Path(__file__).parent / "ports.csv"
    ports = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key  = row["search_key"].strip().lower()
            lat  = float(row["latitude"])
            lon  = float(row["longitude"])
            name = row["display_name"].strip()
            ports[key] = (lat, lon, name)
    return ports


PORTS = load_ports()

def get_unique_ports():
    seen = {}
    for key, (lat, lon, name) in PORTS.items():
        if name not in seen:
            seen[name] = (lat, lon)
    return seen

UNIQUE_PORTS = get_unique_ports()
ALL_PORT_NAMES = sorted(UNIQUE_PORTS.keys())

def search_ports(query):
    query = query.strip().lower()
    if not query:
        return []

    matches = []
    for name in ALL_PORT_NAMES:
        if query in name.lower():
            matches.append(name)

    for key, (lat, lon, name) in PORTS.items():
        if query in key and name not in matches:
            matches.append(name)

    return sorted(matches)


def get_beaufort(wind_kmh):
    scale = [
        (1,   0,  "Calm"),
        (5,   1,  "Light air"),
        (11,  2,  "Light breeze"),
        (19,  3,  "Gentle breeze"),
        (28,  4,  "Moderate breeze"),
        (38,  5,  "Fresh breeze"),
        (49,  6,  "Strong breeze"),
        (61,  7,  "Near gale"),
        (74,  8,  "Gale"),
        (88,  9,  "Strong gale"),
        (102, 10, "Storm"),
        (117, 11, "Violent storm"),
        (999, 12, "Hurricane"),
    ]
    for max_speed, bft_num, description in scale:
        if wind_kmh <= max_speed:
            return bft_num, description
    return 12, "Hurricane"

def degrees_to_compass(deg):
    if deg is None:
        return "N/A"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(deg / 22.5) % 16
    return directions[index]

def check_for_alerts(weather):
    alerts = []

    wind_speed  = weather.get("wind_kmh", 0) or 0
    visibility  = weather.get("visibility_km", 10) or 10
    wave_height = weather.get("wave_height_m")
    rain        = weather.get("precipitation_mm", 0) or 0

    bft, _ = get_beaufort(wind_speed)
    if bft >= 8:
        alerts.append(("CRITICAL", f"Gale-force winds — Beaufort {bft} — vessel ops unsafe"))
    elif bft >= 6:
        alerts.append(("WARNING",  f"Strong winds — Beaufort {bft} — use caution on deck"))
    elif bft >= 5:
        alerts.append(("ADVISORY", f"Fresh breeze — Beaufort {bft} — monitor conditions"))

    if visibility < 0.5:
        alerts.append(("CRITICAL", f"Dense fog — visibility only {visibility:.1f} km"))
    elif visibility < 1.0:
        alerts.append(("WARNING",  f"Thick fog — visibility {visibility:.1f} km"))
    elif visibility < 3.0:
        alerts.append(("ADVISORY", f"Poor visibility — {visibility:.1f} km"))

    if wave_height is not None:
        if wave_height >= 4.0:
            alerts.append(("CRITICAL", f"Very rough seas — {wave_height:.1f} m waves"))
        elif wave_height >= 2.5:
            alerts.append(("WARNING",  f"Rough seas — {wave_height:.1f} m waves"))
        elif wave_height >= 1.25:
            alerts.append(("ADVISORY", f"Moderate swell — {wave_height:.1f} m"))

    if rain >= 10:
        alerts.append(("WARNING",  f"Heavy rain — {rain:.1f} mm/h"))
    elif rain >= 2:
        alerts.append(("ADVISORY", f"Moderate rain — {rain:.1f} mm/h"))

    return alerts

def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        "precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,"
        "wind_gusts_10m,visibility,surface_pressure"
        "&hourly=wave_height,wave_direction,wave_period,"
        "swell_wave_height,swell_wave_direction,swell_wave_period,wind_wave_height"
        "&wind_speed_unit=kmh"
        "&timezone=auto"
        "&forecast_days=1"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    current = data["current"]
    hourly  = data.get("hourly", {})

    current_time_prefix = current["time"][:13]
    time_list   = hourly.get("time", [])
    hour_index  = 0
    for i, t in enumerate(time_list):
        if t.startswith(current_time_prefix):
            hour_index = i
            break

    def get_hourly(key):
        values = hourly.get(key, [])
        if values and hour_index < len(values):
            return values[hour_index]
        return None

    wmo_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Heavy drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        77: "Snow grains",
        80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
        95: "Thunderstorm", 96: "Thunderstorm + hail", 99: "Thunderstorm + heavy hail",
    }

    raw_visibility = current.get("visibility")
    visibility_km  = raw_visibility / 1000 if raw_visibility is not None else 10.0

    weather = {
        "temperature_c"      : current.get("temperature_2m"),
        "feels_like_c"       : current.get("apparent_temperature"),
        "humidity_pct"       : current.get("relative_humidity_2m"),
        "wind_kmh"           : current.get("wind_speed_10m"),
        "wind_dir_deg"       : current.get("wind_direction_10m"),
        "wind_gusts_kmh"     : current.get("wind_gusts_10m"),
        "visibility_km"      : visibility_km,
        "cloud_cover_pct"    : current.get("cloud_cover"),
        "pressure_hpa"       : current.get("surface_pressure"),
        "precipitation_mm"   : current.get("precipitation"),
        "conditions"         : wmo_codes.get(current.get("weather_code"), "Unknown"),
        "wave_height_m"      : get_hourly("wave_height"),
        "wave_dir_deg"       : get_hourly("wave_direction"),
        "wave_period_s"      : get_hourly("wave_period"),
        "swell_height_m"     : get_hourly("swell_wave_height"),
        "swell_dir_deg"      : get_hourly("swell_wave_direction"),
        "swell_period_s"     : get_hourly("swell_wave_period"),
        "wind_wave_height_m" : get_hourly("wind_wave_height"),
        "observed_at"        : current.get("time"),
        "timezone"           : data.get("timezone"),
    }

    return weather

def wind_color_class(bft):
    if bft <= 3:   return "green"
    elif bft <= 5: return "green"
    elif bft <= 7: return "amber"
    elif bft <= 9: return "orange"
    else:          return "red"

def vis_color_class(km):
    if km >= 5:   return "green"
    elif km >= 1: return "amber"
    else:         return "red"

def wave_color_class(m):
    if m is None:  return ""
    if m < 1.25:   return "green"
    elif m < 2.5:  return "amber"
    elif m < 4.0:  return "orange"
    else:          return "red"


def stat_row(label, value, css_class=""):
    return f"""
    <div class="stat-row">
        <span class="stat-label">{label}</span>
        <span class="stat-value {css_class}">{value}</span>
    </div>"""


def section_card(title, rows_html):
    return f"""
    <div class="section-card">
        <div class="section-title">{title}</div>
        {rows_html}
    </div>"""


st.markdown("""
<div class="hero-header">
    <div class="hero-title">PORT WEATHER CHECKER</div>
    <div class="hero-subtitle">Real-time marine conditions for dispatch engineers</div>
</div>
""", unsafe_allow_html=True)


col_search, col_gap = st.columns([3, 1])

with col_search:
    st.markdown('<div class="search-label">Type a port name</div>', unsafe_allow_html=True)
    search_query = st.text_input(
        label="port search",
        label_visibility="collapsed",
        placeholder="e.g.  Singapore,  Klang,  Mumbai,  Shanghai...",
        key="port_search",
    )

matching_ports = []
if search_query and search_query.strip():
    matching_ports = search_ports(search_query)

selected_port = None

if matching_ports:
    st.markdown('<div class="search-label" style="margin-top:1rem;">Select the port</div>', unsafe_allow_html=True)
    selected_port = st.selectbox(
        label="port select",
        label_visibility="collapsed",
        options=matching_ports,
        key="port_select",
    )
elif search_query and search_query.strip():
    st.markdown('<div class="no-results">No ports found — try a shorter or different name</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
btn_col, _ = st.columns([1, 3])
with btn_col:
    check_clicked = st.button("Check Conditions", key="check_btn")


if check_clicked and selected_port:

    lat, lon = UNIQUE_PORTS[selected_port]

    with st.spinner(f"Fetching live weather for {selected_port}..."):
        try:
            weather = fetch_weather(lat, lon)
        except Exception as e:
            st.error(f"Could not fetch weather data: {e}")
            st.stop()

    alerts = check_for_alerts(weather)
    observed = weather.get("observed_at", "N/A")
    timezone = weather.get("timezone", "UTC")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-bottom:1.2rem;">
        <div class="port-name-header">{selected_port}</div>
        <div class="port-meta">
            {lat:.4f}°, {lon:.4f}° &nbsp;·&nbsp; Observed: {observed} [{timezone}]
        </div>
    </div>
    """, unsafe_allow_html=True)

    highest_level = None
    for level, _ in alerts:
        if level == "CRITICAL":
            highest_level = "CRITICAL"
            break
        elif level == "WARNING":
            highest_level = "WARNING"

    if highest_level == "CRITICAL":
        st.markdown("""
        <div class="verdict-critical">
            <div class="verdict-icon">🚨</div>
            <div class="verdict-title critical">DO NOT DISPATCH</div>
            <div class="verdict-sub">Critical conditions detected — port operations unsafe</div>
        </div>
        """, unsafe_allow_html=True)
    elif highest_level == "WARNING":
        st.markdown("""
        <div class="verdict-warning">
            <div class="verdict-icon">⚠️</div>
            <div class="verdict-title warning">PROCEED WITH CAUTION</div>
            <div class="verdict-sub">Adverse conditions — review alerts before dispatch</div>
        </div>
        """, unsafe_allow_html=True)
    elif alerts:
        st.markdown("""
        <div class="verdict-warning">
            <div class="verdict-icon">ℹ️</div>
            <div class="verdict-title warning">ADVISORY IN EFFECT</div>
            <div class="verdict-sub">Minor conditions noted — monitor before and during ops</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="verdict-safe">
            <div class="verdict-icon">✅</div>
            <div class="verdict-title safe">ALL CLEAR</div>
            <div class="verdict-sub">Conditions are safe — safe to dispatch</div>
        </div>
        """, unsafe_allow_html=True)

    if alerts:
        alerts_html = ""
        for level, message in alerts:
            css   = level.lower()
            icon  = "✖" if level == "CRITICAL" else ("⚠" if level == "WARNING" else "ℹ")
            alerts_html += f"""
            <div class="alert-pill {css}">
                <span class="alert-badge">{icon} {level}</span>
                <span>{message}</span>
            </div>"""
        st.markdown(f"""
        <div class="section-card">
            <div class="section-title">Operational Alerts</div>
            {alerts_html}
        </div>
        """, unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    temp        = weather.get("temperature_c")
    feels       = weather.get("feels_like_c")
    humidity    = weather.get("humidity_pct")
    pressure    = weather.get("pressure_hpa")
    cloud       = weather.get("cloud_cover_pct")
    conditions  = weather.get("conditions", "N/A")

    wind_speed  = weather.get("wind_kmh")
    wind_gusts  = weather.get("wind_gusts_kmh")
    wind_dir    = weather.get("wind_dir_deg")
    visibility  = weather.get("visibility_km")
    rain        = weather.get("precipitation_mm")

    wave_h      = weather.get("wave_height_m")
    wave_dir    = weather.get("wave_dir_deg")
    wave_per    = weather.get("wave_period_s")
    swell_h     = weather.get("swell_height_m")
    swell_dir   = weather.get("swell_dir_deg")
    swell_per   = weather.get("swell_period_s")
    wind_wave_h = weather.get("wind_wave_height_m")

    bft_num, bft_desc = get_beaufort(wind_speed or 0)

    with left_col:

        atmo_rows = stat_row("Sky", conditions)
        if temp is not None:
            feels_str = f"{feels:.1f} °C" if feels is not None else "N/A"
            atmo_rows += stat_row("Temperature", f"{temp:.1f} °C")
            atmo_rows += stat_row("Feels like", feels_str)
        if humidity is not None:
            atmo_rows += stat_row("Humidity", f"{humidity:.0f} %")
        if pressure is not None:
            atmo_rows += stat_row("Pressure", f"{pressure:.0f} hPa")
        if cloud is not None:
            atmo_rows += stat_row("Cloud cover", f"{cloud:.0f} %")
        st.markdown(section_card("☁️  Atmosphere", atmo_rows), unsafe_allow_html=True)

        vis_rows = ""
        if visibility is not None:
            vis_rows += stat_row("Visibility", f"{visibility:.1f} km", vis_color_class(visibility))
        if rain is not None:
            rain_css = "amber" if rain >= 2 else "green"
            vis_rows += stat_row("Precipitation", f"{rain:.1f} mm/h", rain_css)
        if not vis_rows:
            vis_rows = stat_row("Visibility", "N/A")
        st.markdown(section_card("🌧️  Visibility & Rain", vis_rows), unsafe_allow_html=True)

    with right_col:

        wind_css = wind_color_class(bft_num)
        wind_rows = ""
        if wind_speed is not None:
            wind_ms = wind_speed / 3.6
            wind_rows += stat_row("Speed", f"{wind_speed:.1f} km/h  ({wind_ms:.1f} m/s)", wind_css)
            wind_rows += stat_row("Beaufort", f"BFT {bft_num} — {bft_desc}", wind_css)
        if wind_gusts is not None:
            wind_rows += stat_row("Gusts", f"{wind_gusts:.1f} km/h", "amber" if wind_gusts > 40 else "")
        if wind_dir is not None:
            compass = degrees_to_compass(wind_dir)
            wind_rows += stat_row("Direction", f"{compass}  ({wind_dir:.0f}°)")
        if not wind_rows:
            wind_rows = stat_row("Wind", "N/A")
        st.markdown(section_card("💨  Wind", wind_rows), unsafe_allow_html=True)

        sea_rows = ""
        if wave_h is not None:
            w_dir_str = degrees_to_compass(wave_dir)
            w_per_str = f"{wave_per:.1f} s" if wave_per else "N/A"
            sea_rows += stat_row("Wave height",  f"{wave_h:.2f} m", wave_color_class(wave_h))
            sea_rows += stat_row("Wave direction", w_dir_str)
            sea_rows += stat_row("Wave period",  w_per_str)
        if swell_h is not None:
            s_dir_str = degrees_to_compass(swell_dir)
            s_per_str = f"{swell_per:.1f} s" if swell_per else "N/A"
            sea_rows += stat_row("Swell height",  f"{swell_h:.2f} m", wave_color_class(swell_h))
            sea_rows += stat_row("Swell direction", s_dir_str)
            sea_rows += stat_row("Swell period",  s_per_str)
        if wind_wave_h is not None:
            sea_rows += stat_row("Wind waves", f"{wind_wave_h:.2f} m", wave_color_class(wind_wave_h))
        if not sea_rows:
            sea_rows = stat_row("Sea state", "Data not available for this location")
        st.markdown(section_card("🌊  Sea State", sea_rows), unsafe_allow_html=True)

elif check_clicked and not selected_port:
    st.warning("Please type a port name and select it from the dropdown first.")
