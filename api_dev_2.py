import numpy as np
import statistics
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def get_water_proximity_data(latitude, longitude):
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://flood-api.open-meteo.com/v1/flood"
  params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2023-09-13",
    "end_date": "2024-09-13",
    "daily": "river_discharge"
  }
  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

  # Process daily data. The order of variables needs to be the same as requested.
  daily = response.Daily()
  daily_river_discharge = daily.Variables(0).ValuesAsNumpy()

  daily_data = {"date": pd.date_range(
    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
    freq = pd.Timedelta(seconds = daily.Interval()),
    inclusive = "left"
  )}
  daily_data["river_discharge"] = daily_river_discharge

  return {"water_proximity": daily_river_discharge}
def get_rain_data(latitude, longiture):
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://archive-api.open-meteo.com/v1/archive"
  params = {
    "latitude": latitude,
    "longitude": longiture,
    "start_date": "2023-09-13",
    "end_date": "2024-09-13",
    "hourly": ["rain", "soil_moisture_7_to_28cm"]
  }
  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

  # Process hourly data. The order of variables needs to be the same as requested.
  hourly = response.Hourly()
  hourly_rain = hourly.Variables(0).ValuesAsNumpy()
  hourly_soil_moisture_7_to_28cm = hourly.Variables(1).ValuesAsNumpy()

  hourly_data = {"date": pd.date_range(
    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
    freq = pd.Timedelta(seconds = hourly.Interval()),
    inclusive = "left"
  )}
  hourly_data["rain"] = hourly_rain
  hourly_data["soil_moisture_7_to_28cm"] = hourly_soil_moisture_7_to_28cm

  return {"rain": hourly_rain, "soil_moisture_7_to_28cm": hourly_soil_moisture_7_to_28cm}

def get_archive_data (latitude, longitude):
   values = get_rain_data(latitude, longitude)
   water_prox_values = get_water_proximity_data(latitude, longitude)

   max_rain_value = get_max_value(values["rain"])
   avg_rain_value = statistics.mean(values["rain"])
   avg_soil_moisture_value = statistics.mean(values["soil_moisture_7_to_28cm"])
   avg_water_prox_value = statistics.mean(water_prox_values["water_proximity"])

   print({
      "max_rain": max_rain_value,
      "avg_rain": avg_rain_value,
      "avg_soil_moisture": avg_soil_moisture_value,
      "avg_water_prox": avg_water_prox_value
      })
  #  print(water_prox_values)

def get_max_value(data):
  a = np.array(data)
  return data[a.argmax()]

if __name__ == '__main__':
    get_archive_data(59.91, 10.75)