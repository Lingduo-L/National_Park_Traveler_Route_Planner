import googlemaps
from flask import Flask, render_template, request, Markup
from park_coordinates import get_park_coordinates
from park_weather import get_park_weather, get_park_info
from draw_result_map import draw_route_in_html
from get_park_info import get_park_info

import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")

# from draw_result_map import compare_city_names

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


GOOGLE_MAPS_API_KEY = google_api_key

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/route_map', methods=['POST'])
def route_map():
    # 从表单获取用户选择的出行模式
    mode = request.form.get("mode")

    origin = request.form.get("origin")  # 获取用户输入的起点
    destination = request.form.get("destination_park")  # 获取用户输入的目的地国家公园

    # 使用Google Maps API的geocode()方法获取起点的坐标
    gmaps = googlemaps.Client(key=google_api_key)
    geocode_result = gmaps.geocode(origin)
    if geocode_result:
        print("get geocode result: ",geocode_result)
        start_lat = geocode_result[0]["geometry"]["location"]["lat"]
        start_lng = geocode_result[0]["geometry"]["location"]["lng"]
    else:
        return "Error: Unable to find the starting location. Please try again with a valid origin address."

    # 以下代码是获取终点国家公园的坐标
    destination_park = get_park_coordinates(destination)
    park_info = get_park_info(destination)


    if destination_park is None:
        return "Error: No matching park found. Please try again with a valid park name."

    # 以下代码是调用Google Maps API获取导航数据，并将其转换为HTML格式
    gmaps = googlemaps.Client(key=google_api_key)

    # directions = gmaps.directions(origin, destination_park, mode="driving")
    # 使用用户选择的模式获取导航数据
    directions = gmaps.directions(origin, destination_park, mode=mode)

    if not directions:
        return "Error: Unable to find directions. Please try again with a valid origin address."
    
    # 提取行程时间
    travel_time = directions[0]['legs'][0]['duration']['text']

    # 生成地图HTML
    map_html = draw_route_in_html(directions)


    # 获取公园天气数据并传递给模板
    park_weather = get_park_weather(destination)

    # Generate the map_html here, using the draw_route_in_html() function
    map_html = draw_route_in_html(directions)

    # return render_template("route_map.html", map_html=Markup(map_html), park_weather=park_weather, travel_time=travel_time)
    # return render_template("route_map.html", map_html=Markup(map_html), park_weather=park_weather, park_weather_length=len(park_weather['next_week_weather']))
    return render_template("route_map.html", map_html=Markup(map_html), park_weather=park_weather, park_weather_length=len(park_weather['next_week_weather']), travel_time=travel_time, park_info=park_info, google_api_key=google_api_key)


    # return render_template("route_map.html", map_html=Markup(map_html), park_weather=park_weather)
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

