#!/usr/bin/env python

#
# See __doc__ for an explanation of what this module does
#
# See __usage__ for an explanation of runtime arguments.
#
# -Christopher Blunck
#

import sys, math, urllib, json
import numpy as np


__author__ = 'Christopher Blunck'
__email__ = 'chris@wxnet.org'
__revision__ = '$Revision: 1.6 $'

__doc__ = 'temperature related conversionfunctions'
__usage__ = 'this module should not be run via the command line'



def celsius_to_fahrenheit(c):
    'Degrees Celsius (C) to degrees Fahrenheit (F)'
    return (c * 1.8) + 32.0

def celsius_to_kelvin(c):
    'Degrees Celsius (C) to degrees Kelvin (K)'
    return c + 273.15

def celsius_to_rankine(c):
    'Degrees Celsius (C) to degrees Rankine (R)'
    return (c * 1.8) + 491.67

def fahrenheit_to_celsius(f):
    'Degrees Fahrenheit (F) to degrees Celsius (C)'
    return (f - 32.0) * 0.555556

def fahrenheit_to_kelvin(f):
    'Degrees Fahrenheit (F) to degrees Kelvin (K)'
    return (f * 0.555556) + 255.37

def fahrenheit_to_rankine(f):
    'Degrees Fahrenheit (F) to degrees Rankine (R)'
    return f + 459.67

def kelvin_to_celsius(k):
    'Degrees Kelvin (K) to degrees Celsius (C)'
    return k - 273.15

def kelvin_to_fahrenheit(k):
    'Degrees Kelvin (K) to degrees Fahrenheit (F)'
    return (k - 255.37) * 1.8

def kelvin_to_rankine(k):
    'Degrees Kelvin (K) to degrees Rankine (R)'
    return k * 1.8

def rankine_to_celsius(r):
    'Degrees Rankine (R) to degrees Celsius (C)'
    return (r - 491.67) * 0.555556

def rankine_to_fahrenheit(r):
    'Degrees Rankine (R) to degrees Fahrenheit (F)'
    return r - 459.67

def rankine_to_kelvin(r):
    'Degrees Rankine (R) to degrees Kelvin (K)'
    return r * 0.555556


def calc_heat_index(temp, hum):
    '''
    calculates the heat index based upon temperature (in F) and humidity.
    http://www.srh.noaa.gov/bmx/tables/heat_index.html

    returns the heat index in degrees F.
    '''

    if (temp < 80):
        return temp
    else:
        return -42.379 + 2.04901523 * temp + 10.14333127 * hum - 0.22475541 * \
               temp * hum - 6.83783 * (10 ** -3) * (temp ** 2) - 5.481717 * \
               (10 ** -2) * (hum ** 2) + 1.22874 * (10 ** -3) * (temp ** 2) * \
               hum + 8.5282 * (10 ** -4) * temp * (hum ** 2) - 1.99 * \
               (10 ** -6) * (temp ** 2) * (hum ** 2);


def calc_wind_chill(t, windspeed, windspeed10min=None):
    '''
    calculates the wind chill value based upon the temperature (F) and
    wind.

    returns the wind chill in degrees F.
    '''

    w = max(windspeed10min, windspeed)
    return 35.74 + 0.6215 * t - 35.75 * (w ** 0.16) + 0.4275 * t * (w ** 0.16);


def calc_humidity(temp, dewpoint):
    '''
    calculates the humidity via the formula from weatherwise.org
    return the relative humidity
    '''

    t = fahrenheit_to_celsius(temp)
    td = fahrenheit_to_celsius(dewpoint)

    num = 112 - (0.1 * t) + td
    denom = 112 + (0.9 * t)

    rh = math.pow((num / denom), 8)

    return rh




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

# Tested using data from https://www.wunderground.com/history/airport/EGOS/2016/11/18/DailyHistory.html?req_city=Shrewsbury&req_state=SHR&req_statename=United+Kingdom&reqdb.zip=00000&reqdb.magic=135&reqdb.wmo=03414
# alongside observed data from actual flights
if __name__ == "__main__":
    # Get data from API
    url = "https://api.darksky.net/forecast/e8848df565e76b6eeb0e2cde6883be5b/52.5189846,-2.8909141?exclude=minutely,hourly,flags"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    min_temp = fahrenheit_to_celsius(data["daily"]["data"][0]["temperatureMin"])
    print "Min forecast temperature for the day is {0}C".format(min_temp)
    max_temp = fahrenheit_to_celsius(data["daily"]["data"][0]["temperatureMax"])
    print "Max forecast temperature for the day is {0}C".format(min_temp)
    humidity = data["daily"]["data"][0]["humidity"] * 100
    print "Humidity is {0}%".format(humidity)
    dewpoint_temp = dewpoint_approximation(min_temp, humidity)
    print "Dewpoint temperature is {0} Celsius".format(dewpoint_temp)
    # Calc cloud base
    cloud_base = calc_cloudbase_height(dewpoint_temp, max_temp)
    print "Cloud base is estimated to be {0} foot".format(cloud_base)
