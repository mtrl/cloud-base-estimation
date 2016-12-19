#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, math, urllib, json, plotly
import plotly.plotly as py
from plotly.graph_objs import *
from datetime import datetime
import weatherunitstemp
import numpy as np

# approximation valid for
# 0 degC < T < 60 degC
# 1% < RH < 100%
# 0 degC < Td < 50 degC
# constants
a = 17.271
b = 237.7 # degC
def dewpoint_approximation(T,RH):
    Td = (b * gamma(T,RH)) / (a - gamma(T,RH))
    return Td

def gamma(T,RH):
    g = (a * T / (b + T)) + np.log(RH/100.0)
    return g

def calc_cloudbase_height(dewpoint, max_day_temp):
    '''
    calculates the cloudbase height based on
    https://en.wikipedia.org/wiki/Cloud_base
    '''
    return ((max_day_temp - dewpoint) / 2.5) * 1000

def day_forecast(lat, lng, day):
    day = int(day)
    url = "https://api.darksky.net/forecast/{0}/{1},{2}?exclude=minutely,hourly,flags".format(api_key, lat, lng)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    day_data = data["daily"]["data"][day]
    timestamp = day_data["time"]
    humidity = day_data["humidity"] * 100
    dew_point = weatherunitstemp.fahrenheit_to_celsius(day_data["dewPoint"])
    max_temp = weatherunitstemp.fahrenheit_to_celsius(day_data["temperatureMax"])

    utc_time = datetime.fromtimestamp(timestamp)
    cloud_base = calc_cloudbase_height(dew_point, max_temp)

    print "+-----------------------------------------+"
    print("| Cloud base forecast for {0} |".format(utc_time.strftime("%a %m %b %Y")))
    print "+-----------------------------------------+"
    print " Estimated cloud base:        {0} ft AGL".format(int(cloud_base))
    print " Maximum temperature:         {:.1f}°C".format(max_temp)
    print " Dew point temperature:       {:.1f}°C".format(dew_point)
    print " Humidity:                    {:.0f}%".format(humidity)
    print "+-----------------------------------------+"

def hourly_forecast(lat, lng):
    url = "https://api.darksky.net/forecast/{0}/{1},{2}?exclude=minutely,daily,flags,events".format(api_key, lat, lng)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    hourly_data = data["hourly"]["data"]

    print "+-----------------------------------------+"
    print "| Hourly cloud base forecast              |"
    print "+-----------------------------------------+"

    y_vals = []
    x_vals = []
    for hour in hourly_data:
        timestamp = hour["time"]
        humidity = hour["humidity"] * 100
        dew_point = weatherunitstemp.fahrenheit_to_celsius(hour["dewPoint"])
        temp = weatherunitstemp.fahrenheit_to_celsius(hour["temperature"])

        utc_time = datetime.fromtimestamp(timestamp)
        cloud_base = calc_cloudbase_height(dew_point, temp)

        nice_time = int(utc_time.strftime("%Y%m%d%H%M"))

        y_vals.append(cloud_base)
        x_vals.append(utc_time)

        print "{0} {1} ft AGL".format(nice_time, int(cloud_base))

    return x_vals, y_vals

def graph_cloud_base(x, y):
    trace0 = Scatter(
        x=x,
        y=y
    )

    data = Data([trace0])
    layout = dict(title = 'Estimated cloud base for {0}, {1}'.format(lat, lng),
              xaxis = dict(title = 'Day'),
              yaxis = dict(title = 'Estimated cloud base (Feet)'),
              )
    fig = dict(data = data, layout = layout)
    py.iplot(fig, filename = 'basic-line')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        sys.exit()
    lat = sys.argv[2] if len(sys.argv) > 2 else "52.5189846"
    lng = sys.argv[3] if len(sys.argv) > 3 else "-2.8909141"
    day = sys.argv[4] if len(sys.argv) > 4 else 0
    if day == "hourly":
        x, y = hourly_forecast(lat=lat, lng=lng)
        # Do we have a plotly username and API key?
        if len(sys.argv) > 6:
            plotly_user = sys.argv[5]
            plotly_key = sys.argv[6]
            plotly.tools.set_credentials_file(username=plotly_user, api_key=plotly_key)
            graph_cloud_base(x, y)
    else:
        day_forecast(lat=lat, lng=lng, day=day)
