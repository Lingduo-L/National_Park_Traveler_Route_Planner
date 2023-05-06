# import re
# import requests
# from typing import Optional
# import json

# def get_park_info() -> dict:
#     parks = dict()
#     with open('parks_cleaned.tsv', encoding='utf8') as file:
#         next(file)  # Skip the header line
#         for line in file:
#             data = line.split('\t')
#             if len(data) < 5:  # Ensure the line has right elements
#                 continue

#             park_name, coordinates = data[0], data[4].split(';')
#             try:
#                 lat, long = round(float(coordinates[0]),4), round(float(coordinates[1]),4)
#                 parks[park_name] = (lat, long)
#             except ValueError:
#                 parks[park_name] = None
#     return parks


# def get_park_weather(park_name: str) -> Optional[dict]:
#     # get name and coord of park
#     parks = get_park_info()

#     matched_park_names = [name for name in parks.keys() if re.search(park_name.lower(), name.lower())]

#     if not matched_park_names:
#         return None

#     if len(matched_park_names) > 1:
#         print(f"Found multiple matching parks: {', '.join(matched_park_names)}")
#         print("Please specify the exact park name.")
#         return None

#     matched_park_name = matched_park_names[0]

#     if parks[matched_park_name] is None:
#         return "Unable to obtain specific coordinates and weather information. Please try another area.\n** Note: you may be searching for a trail or National Parkway that spans multiple regions."

#     # get weather API data
#     lat, long = parks[matched_park_name]
#     url = f"https://api.weather.gov/points/{lat},{long}"

#     try:
#         response = requests.get(url, headers={'User-Agent': 'park_weather'})
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         return f"Error: Unable to get park coordinates data. {str(e)}"

#     try:
#         posts = response.json()
#         wthr_forecast_url = posts["properties"]["forecast"]  # get the forecast of next few days

#         try:
#             wthr_forecast_response = requests.get(wthr_forecast_url)
#             wthr_forecast_response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             return f"Error: Unable to get weather forecast data. {str(e)}"

#         try:
#             next_week_posts = wthr_forecast_response.json()
#             next_week_pridict = [next_week_posts["properties"]["periods"][i]["shortForecast"] for i in range(14)]
#             weather_data = {
#                 "park_name": matched_park_name,
#                 "next_week_weather": next_week_pridict
#             }
#             return weather_data
#         except Exception as e:
#             return f"Unable to obtain next week forecast: {str(e)}"
#     except Exception as e:
#         return f"Unable to obtain weather data: {str(e)}"

# def save_all_park_weather_to_json():
#     parks = get_park_info()
#     all_park_weather_data = {}

#     for park_name in parks.keys():
#         weather_data = get_park_weather(park_name)

#         if weather_data is not None:
#             all_park_weather_data[park_name] = weather_data
#             print(park_name," finished!")

#     # Save the weather data of all parks to a single JSON file
#     with open("all_park_weather_data'.json", 'w', encoding='utf-8') as f:
#         json.dump(all_park_weather_data, f, ensure_ascii=False, indent=4)

# # Call the function to save the weather data for all parks in a single JSON file
# save_all_park_weather_to_json()


import re
import requests
from typing import Optional
import json

def get_park_info() -> dict:
    parks = dict()
    with open('parks_cleaned.tsv', encoding='utf8') as file:
        next(file)  # Skip the header line
        for line in file:
            data = line.split('\t')
            if len(data) < 5:  # Ensure the line has right elements
                continue

            park_name, coordinates = data[0], data[4].split(';')
            try:
                lat, long = round(float(coordinates[0]),4), round(float(coordinates[1]),4)
                parks[park_name] = (lat, long)
            except ValueError:
                parks[park_name] = None
    return parks

def get_park_weather(park_name: str) -> Optional[dict]:
    # get name and coord of park
    parks = get_park_info()

    matched_park_names = [name for name in parks.keys() if re.search(park_name.lower(), name.lower())]

    if not matched_park_names:
        return None

    if len(matched_park_names) > 1:
        print(f"Found multiple matching parks: {', '.join(matched_park_names)}")
        print("Please specify the exact park name.")
        return None

    matched_park_name = matched_park_names[0]

    if parks[matched_park_name] is None:
        return "Unable to obtain specific coordinates and weather information. Please try another area.\n** Note: you may be searching for a trail or National Parkway that spans multiple regions."

    # get weather API data
    lat, long = parks[matched_park_name]
    url = f"https://api.weather.gov/points/{lat},{long}"

    try:
        response = requests.get(url, headers={'User-Agent': 'park_weather'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to get park coordinates data. {str(e)}"

    try:
        posts = response.json()
        wthr_forecast_url = posts["properties"]["forecast"]  # get the forecast of next few days

        try:
            wthr_forecast_response = requests.get(wthr_forecast_url)
            wthr_forecast_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error: Unable to get weather forecast data. {str(e)}"

        try:
            next_week_posts = wthr_forecast_response.json()
            next_week_pridict = [next_week_posts["properties"]["periods"][i]["shortForecast"] for i in range(14)]
            weather_data = {
                "park_name": matched_park_name,
                "next_week_weather": next_week_pridict
            }
            return weather_data
        except Exception as e:
            return f"Unable to obtain next week forecast: {str(e)}"
    except Exception as e:
        return f"Unable to obtain weather data: {str(e)}"

def save_all_park_weather_to_json():
    parks = get_park_info()
    all_park_weather_data = {}

    for park_name in parks.keys():
        weather_data = get_park_weather(park_name)

        if weather_data is not None:
            all_park_weather_data[park_name] = weather_data
            print(park_name," finished!")

    # Save the weather data of all parks to a single JSON file
    with open("all_park_weather_data.json", 'w', encoding='utf-8') as f:
        json.dump(all_park_weather_data, f, ensure_ascii=False, indent=4)

# Call the function to save the weather data for all parks in a single JSON file
# save_all_park_weather_to_json()

