"""A module to retrieve various weather data from Hong Kong Observatory"""

import json
import pkg_resources
import re
from operator import itemgetter
import requests

from hko.distance_calculation import distance_calculation

# Load required JSON data
with open(pkg_resources.resource_filename(__name__, 'assets/grid_location.json')) as f:
    GRID = json.load(f)
with open(pkg_resources.resource_filename(__name__, 'assets/rainfall_nowcast_mapping.json')) as f:
    RAINFALL_MAPPING = json.load(f)

# Base URLs
HKO_PDA_URL = 'http://pda.weather.gov.hk/'
HKO_WEB_URL = 'http://www.weather.gov.hk/'

def local_weather(lat, lng):
    """Retrieve local weather data from Hong Kong Observatory
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        dict: Response containing weather data and status
    """
    response = {}
    if isinstance(lat, float) and isinstance(lng, float) and\
       -90 <= lat <= 90 and -180 <= lng <= 180:
        temp_dict = GRID
        for i in temp_dict:
            distance = distance_calculation(lat, lng, float(i['lat']), float(i['lng']))
            i['dis'] = distance
        newlist = sorted(temp_dict, key=itemgetter('dis'))
        if newlist[0]['dis'] < 10:
            try:
                grid = newlist[0]['grid']
                url = 'locspc/android_data/gridData/{}_tc.xml'.format(grid)
                grid_data = json.loads(requests.get(HKO_PDA_URL + url).text)
                response['status'] = 1
                response['result'] = grid_data
                response['place'] = newlist[0]['name']
            except IndexError:
                response['result'] = ''
                response['status'] = 2
            except requests.exceptions.RequestException:
                response['result'] = ''
                response['status'] = 5
        else:
            response['result'] = ''
            response['status'] = 3
    else:
        response['result'] = ''
        response['status'] = 0
    return response

def rainfall_nowcast(lat, lng):
    """Retrieve rainfall nowcast data from Hong Kong Observatory
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        dict: Response containing rainfall forecast data and status
    """
    response = {}
    if isinstance(lat, float) and isinstance(lng, float) and\
       -90 <= lat <= 90 and -180 <= lng <= 180:
        temp_dict = RAINFALL_MAPPING
        for i in temp_dict:
            distance = distance_calculation(lat, lng, float(i['lat']), float(i['lng']))
            i['dis'] = distance
        newlist = sorted(temp_dict, key=itemgetter('dis'))
        if newlist[0]['dis'] > 10:
            response['result'] = ''
            response['status'] = 3
            return response
        lat_2 = newlist[0]['lat']
        lng_2 = newlist[0]['lng']
        try:
            url = 'locspc/android_data/rainfallnowcast/{}_{}.xml'.format(float(lat_2), float(lng_2))
            data = requests.get(HKO_PDA_URL + url).content
            data2 = re.split('[@#]', data.decode('utf-8'))
            temp = {}
            temp['0-30'] = {'from_time': data2[0], 'to_time': data2[2], 'value': data2[1]}
            temp['30-60'] = {'from_time': data2[2], 'to_time': data2[4], 'value': data2[3]}
            temp['60-90'] = {'from_time': data2[4], 'to_time': data2[6], 'value': data2[5]}
            temp['90-120'] = {'from_time': data2[6], 'to_time': data2[8], 'value': data2[7]}
            temp['description_en'] = data2[9]
            temp['description_tc'] = data2[10]
            temp['description_sc'] = data2[11]
            response['result'] = temp
            response['status'] = 1
        except IndexError:
            response['result'] = ''
            response['status'] = 2
        except requests.exceptions.RequestException:
            response['result'] = ''
            response['status'] = 5
    else:
        response['result'] = ''
        response['status'] = 0
    return response

def uv_index(lang='UC'):
    """Retrieve UV index data from Hong Kong Observatory
    
    Args:
        lang (str): Language code ('UC' for Traditional Chinese, 'EN' for English)
        
    Returns:
        dict: Response containing UV index data and status
    """
    response = {}
    if lang in ['UC', 'EN']:
        try:
            if lang == 'UC':
                data = requests.get(HKO_PDA_URL + 'locspc/android_data/fuvc.xml').content.decode('utf8')
                data_1 = data.split(u'的最高紫外線指數大約是')
                response['result'] = {}
                response['result']['date'] = data_1[0]
                response['result']['max_uv_index'] = data_1[1].split(u'，強度屬於')[0]
                response['result']['intensity'] = data_1[1].split(u'，強度屬於')[1][:-1]
                response['status'] = 1
            if lang == 'EN':
                data = requests.get(HKO_PDA_URL + 'locspc/android_data/fuve.xml').content.decode('utf8')
                data_1 = data.replace('The maximum UV Index for ', '')\
                             .replace(' will be about ', ',')\
                             .replace('. The intensity of UV radiation wll be ', ',')[:-1]
                data_2 = data_1.split(',')
                response['result'] = {}
                response['result']['date'] = data_2[0]
                response['result']['max_uv_index'] = data_2[1]
                response['result']['intensity'] = data_2[2]
                response['status'] = 1
        except IndexError:
            if data:
                response['result'] = data
                response['status'] = 4
            else:
                response['result'] = ''
                response['status'] = 2
        except requests.exceptions.RequestException:
            response['result'] = ''
            response['status'] = 5
    else:
        response['result'] = ''
        response['status'] = 0
    return response

def weather_warning(lang='UC'):
    """Retrieve weather warning data from Hong Kong Observatory
    
    Args:
        lang (str): Language code ('UC' for Traditional Chinese, 'EN' for English)
        
    Returns:
        dict: Response containing weather warning data and status
    """
    response = {}
    if lang in ['UC', 'EN']:
        try:
            if lang == 'UC':
                data = requests.get(HKO_WEB_URL + 'wxinfo/json/warnsumc.xml')
            if lang == 'EN':
                data = requests.get(HKO_WEB_URL + 'wxinfo/json/warnsum.xml')
            data_2 = json.loads(data.text.replace('var weather_warning_summary = ', '')[:-2] + '}')
            response['result'] = data_2
            response['status'] = 1
        except IndexError:
            response['result'] = ''
            response['status'] = 2
        except requests.exceptions.RequestException:
            response['result'] = ''
            response['status'] = 5
    else:
        response['result'] = ''
        response['status'] = 0
    return response

def several_days_weather_forecast(lang='UC'):
    """Retrieve several days weather forecast data from Hong Kong Observatory
    
    Args:
        lang (str): Language code ('UC' for Traditional Chinese, 'EN' for English)
        
    Returns:
        dict: Response containing several days weather forecast data and status
    """
    response = {}
    if lang in ['UC', 'EN']:
        try:
            url = 'locspc/android_data/fnd_uc.xml' if lang == 'UC' else 'locspc/android_data/fnd_e.xml'
            data = json.loads(requests.get(HKO_PDA_URL + url).content)
            response['result'] = data
            response['status'] = 1
        except IndexError:
            response['result'] = ''
            response['status'] = 2
        except requests.exceptions.RequestException:
            response['result'] = ''
            response['status'] = 5
    else:
        response['result'] = ''
        response['status'] = 0
    return response 