# coding:utf8
import requests
import json


class Weather:
    """
    Acorrding the city_name, return the city_weather_report
    """
    def __init__(self):
        self.auth_key = '4f0b90a529934e65a05cdf32b2d7800a'
        self.weather_url = 'https://api.heweather.com/x3/weather?cityid=%s&key=%s'
        self.city_url = 'https://api.heweather.com/x3/citylist?search=%s&key=%s'
        self.city_id_dict = {}
        self._get_city_id()

    def _get_city_id(self):
        """
        To initialize the city_id_dict
        """
        city_id_result = json.loads(
            requests.get(
                self.city_url % ('allchina', self.auth_key)
            ).text
        )
        for item in city_id_result['city_info']:
            self.city_id_dict[item['city']] = item['id']

    def get_weather_report(self, city_name, weak=None):
        """
        According the city_name, return the weather_report of now or 7 day
        """
        weather = json.loads(
            requests.get(
                self.weather_url % (
                    self.city_id_dict[city_name],
                    self.auth_key
                ),
                verify=True
            ).text
        )
        if weak:
            pass
        else:
            return weather['HeWeather data service 3.0'][0]['now']

c = Weather()
result = c.get_weather_report(u'广州')
print result
for key, value in result['cond'].iteritems():
    print key, value

