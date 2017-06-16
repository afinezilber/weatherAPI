import urllib2
import json
import datetime

### This program prompts the user for City and Country inputs and extracts information from the OpenWeatherMap API
### and displays weather information from the specified zone

class weather(object):

    # Function to convert time to human readability from JSON file
    def time_converter(time):
        converted_time = datetime.datetime.fromtimestamp(int(time)).strftime('%I:%M %p')
        return converted_time

    def convert_celsius(temp):
        temp -= 273.15
        return temp

    def convert_fahrenheit(temp):
        temp = (temp * (9.0)/5) - 459.67
        return temp

    # Prompts user for City and Country inputs and stores them as lower case strings
    city = raw_input("Please insert city name: ").lower()
    city = city.replace(" ", "")
    country = raw_input("Please insert country name code (USA, UK etc..): ").lower();
    country = country.replace(" ", "")

    # URL and API Key stored into variables for string manipulation with user input
    apikey = "9e04457b0a85d0ae24242661ad3a643d"
    url = "http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s" % (city, country, apikey)

    # Checks for 400 Errors and prints appropriate response based on error number
    try:
        response = urllib2.urlopen(url).read()
    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Whoops, Page not found!"
        elif err.code == 403:
            print "Access denied!"
        else:
            print "Whoops, something went wrong. Error code: ", err.code
    except urllib2.URLError, err:
        print "Whoops, error:", err.reason

    # Data extracted from API get request and stored into variables
    data = json.loads(response)
    cityName =  data.get('name')
    countryName = data.get('sys').get('country')
    weather = data['weather'][0]['description']
    fahrenheit = convert_fahrenheit(data.get('main').get('temp'))
    minFah = convert_fahrenheit(data.get('main').get('temp_min'))
    highFah = convert_fahrenheit(data.get('main').get('temp_max'))
    celsius = convert_celsius(data.get('main').get('temp'))
    minCel = convert_celsius(data.get('main').get('temp_min'))
    highCel = convert_celsius(data.get('main').get('temp_max'))
    pressure = data.get('main').get('pressure')
    humidity = data.get('main').get('humidity')
    windspeed = data.get('wind').get('speed')
    windDegree = data.get('deg')
    sunrise = time_converter(data.get('sys').get('sunrise'))
    sunset = time_converter(data.get('sys').get('sunset'))
    timeUpdate = time_converter(data.get('dt'))
    degree_sign= u'\N{DEGREE SIGN}'

    # Prints output for data extraction from JSON file based on user input
    print "========================================================================"
    print "The Weather Report for %s, %s:\n\n" % (cityName, country.upper())
    print "Fahrenheit: %d%cF %s\n(Min: %d%cF  High: %d%cF)\n\n"\
            %(fahrenheit, degree_sign, weather, minFah, degree_sign, highFah, degree_sign)
    print "Celsius:    %d%cC %s \n(Min: %d%cC  High: %d%cC)\n\n"\
            % (celsius, degree_sign, weather, minCel, degree_sign, highCel, degree_sign)
    print "Pressure: %d\nHumidity: %d\nWind Speed: %d\nWind Degree: %s\n\nSunrise: %s\nSunset: %s\n"\
            %(pressure, humidity, windspeed, windDegree, sunrise, sunset)
    print "Information last updated: %s" %(timeUpdate)
    print "========================================================================"
