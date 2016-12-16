#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, math, urllib, json
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

if __name__ == "__main__":
    # Get data from API
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        sys.exit()
    lat = sys.argv[2] if len(sys.argv) > 2 else "52.5189846"
    lng = sys.argv[3] if len(sys.argv) > 3 else "-2.8909141"
    day = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    url = "https://api.darksky.net/forecast/{0}/{1},{2}?exclude=minutely,hourly,flags".format(api_key, lat, lng)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    day_data = data["daily"]["data"][day]
    timestamp = day_data["time"]
    humidity = day_data["humidity"] * 100
    dew_point = weatherunitstemp.fahrenheit_to_celsius(day_data["dewPoint"])
    # min_temp = weatherunitstemp.fahrenheit_to_celsius(day_data["temperatureMin"])
    max_temp = weatherunitstemp.fahrenheit_to_celsius(day_data["temperatureMax"])
    # mean_temp = (max_temp + min_temp) / 2

    utc_time = datetime.fromtimestamp(timestamp)
    # dewpoint_temp = dewpoint_approximation(mean_temp, humidity)
    cloud_base = calc_cloudbase_height(dew_point, max_temp)

    print "+-----------------------------------------+"
    print("| Cloud base forecast for {0} |".format(utc_time.strftime("%a %m %b %Y")))
    print "+-----------------------------------------+"
    print " Estimated cloud base: {0} feet AGL".format(int(cloud_base))
    # print " Mean. temp:            {:.1f}°C".format(mean_temp)
    print " Maximum temperature:  {:.1f}°C".format(max_temp)
    print " Humidity:             {:.0f}%".format(humidity)
    print " Dew point:            {:.1f}°C".format(dew_point)
    print "+-----------------------------------------+"
