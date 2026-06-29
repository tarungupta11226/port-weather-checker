# Port Weather Checker

A real-time marine weather tool built for port dispatch engineers. Type a port name, get live wind speed, wave height, visibility, sea state, and an instant dispatch verdict — all in one screen.

Built with **Python** and **Streamlit**, pulling live data from the **Open-Meteo API**.

---

## What It Does

Before dispatching an engineer to a vessel at port, you need to know the conditions on the ground. This tool gives you:

- **Dispatch verdict** — All Clear / Proceed with Caution / Do Not Dispatch
- **Wind speed & Beaufort scale rating**
- **Wave height, swell height & wave period**
- **Visibility in km**
- **Temperature, humidity, pressure & precipitation**
- **Colour-coded alerts** — Critical, Warning, Advisory

Covers **187 ports** across Singapore, Malaysia, China, India, Vietnam, USA, Indonesia, Thailand, Philippines, Japan, South Korea, Taiwan, Australia and more.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web framework | Streamlit |
| Weather data | Open-Meteo API |
| Port database | CSV file (ports.csv) |
| Language | Python 3.8+ |
| Hosting | Streamlit Community Cloud |

---

## Project Structure

```
.
├── app.py            # Main Streamlit web app
├── ports.csv         # Port database (187 ports, lat/lon, display names)
├── requirements.txt  # Python dependencies
└── README.md
```

---

## How to Run Locally

**Step 1 — Clone the repo**
```bash
git clone https://github.com/tarungupta11226/port-weather-checker.git
cd port-weather-checker
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**
```bash
streamlit run port_weather.py
```

The app opens automatically at `http://localhost:8501`

---

## How to Use the App

1. Type any part of a port name in the search box — e.g. `klang`, `sing`, `mum`, `shanghai`
2. Select the correct port from the dropdown
3. Click **Check Conditions**
4. Read the verdict banner and review the weather cards

---

## How to Add a New Port

Open `ports.csv` and add a new row. No Python changes needed.

```
search_key,latitude,longitude,display_name
my new port,1.3500,103.9500,"My New Port, Singapore"
```

- `search_key` — what users type to find it (lowercase, can be a short nickname)
- `latitude` / `longitude` — decimal degrees
- `display_name` — what shows up in the dropdown and report

You can add multiple search keys pointing to the same port (e.g. `jnpt` and `nhava sheva` both pointing to the same coordinates).

---

## Alert Thresholds

| Condition | Advisory | Warning | Critical |
|---|---|---|---|
| Wind (Beaufort) | BFT 5 | BFT 6–7 | BFT 8+ |
| Visibility | < 3 km | < 1 km | < 0.5 km |
| Wave height | > 1.25 m | > 2.5 m | > 4.0 m |
| Rain | > 2 mm/h | > 10 mm/h | — |

---

## Dependencies

```
streamlit>=1.35.0
requests>=2.31.0
```

---

## Data Source

Weather data is fetched from [Open-Meteo](https://open-meteo.com/) — a free, open-source weather API with no registration or API key required. Data includes current conditions and hourly marine forecasts.
