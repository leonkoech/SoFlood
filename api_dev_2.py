import requests
import os
# from dotenv import load_dotenv, dotenv_values 
import numpy as np
import statistics
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

from ml_stuff import predict_flood_value

def precipitation_average_week(lat,long):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": "2024-09-10",
        "end_date": "2024-09-16",
        "models": ["CMCC_CM2_VHR4", "FGOALS_f3_H", "HiRAM_SIT_HR", "MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR", "NICAM16_8S"],
        "daily": "precipitation_sum"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_precipitation_sum = daily.Variables(0).ValuesAsNumpy()

    return statistics.mean(daily_precipitation_sum) 
     
# load_dotenv()

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

  return {"rain": hourly_rain, "soil_moisture_7_to_28cm": hourly_soil_moisture_7_to_28cm, "elevation": response.Elevation()}

def get_avg_risk_s(zip_code):
    file_path = "estimates.txt"
    with open(file_path, 'r') as file:
        # Skip the first line (header)
        header = file.readline()

        # Loop through each line in the file
        for line in file:
            # Split each line into columns based on space or tab separation
            columns = line.split()

            # Make sure the line has enough columns before processing
            if len(columns) < 5:
                continue

            # Extract relevant values
            current_zip_code = columns[0]
            avg_risk_s = columns[4]

            # If the zip code matches the one we are looking for, print avg_risk_s
            if current_zip_code == zip_code:
                return avg_risk_s

def get_archive_data (zip, latitude, longitude):
   values = get_rain_data(latitude, longitude)
   water_prox_values = get_water_proximity_data(latitude, longitude)

   max_rain_value = get_max_value(values["rain"])
   avg_rain_value = statistics.mean(values["rain"])
   avg_soil_moisture_value = statistics.mean(values["soil_moisture_7_to_28cm"])
   avg_water_prox_value = statistics.mean(water_prox_values["water_proximity"])
   precipitation= precipitation_average_week(52.52,13.41)
   elevation = values["elevation"]

   return {
      "max_rain": max_rain_value,
      "avg_rain": avg_rain_value,
      "avg_soil_moisture": avg_soil_moisture_value,
      "avg_water_prox": avg_water_prox_value,
      "precipitation": precipitation,
      "elevation": elevation,
      'population': get_population_by_zipcode(zip)/10000,
      "FEMA prediction": get_avg_risk_s(str(zip))
      }


def get_population_by_zipcode(zipcode): 
  url = f"https://global.metadapi.com/zipc/v1/zipcodes/{zipcode}"
  headers = {
    "Accept": "application/json",
    "Ocp-Apim-Subscription-Key": "eb6cc2be8848428baa9720be30fd035a"
  }
  response = requests.get(url, headers=headers)
  zipCodeStatistics = response.json()['data']['zipCodeStatistics']

  print(zipCodeStatistics[-1]['totalPopulation'])
  # get the last item in the data array
  return zipCodeStatistics[-1]['totalPopulation']

def get_max_value(data):
  a = np.array(data)
  return data[a.argmax()]

def make_prediction(zip, lat, lng):
   model_values = get_archive_data(zip, lat, lng)
   return predict_flood_value(model_values)


