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
        try:
            weather = json.loads(
                requests.get(
                    self.weather_url % (
                        self.city_id_dict[city_name],
                        self.auth_key
                    ),
                    verify=True
                ).text
            )
        except KeyError:
            return "仅支持中国部分市级城市!"

        if weak:
            pass
        else:
            now_weather = weather['HeWeather data service 3.0'][0]['now']
            now_weather['cond'] = now_weather['cond']['txt']
            now_weather['city'] = city_name
            weather_report = (
                u'城市: {0[city]}\n'
                u'湿度 : {0[hum]}%\n'
                u'降雨量 : {0[pcpn]}mm\n'
                u'天气状况 : {0[cond]}\n'
                u'当前温度 : {0[tmp]}摄氏度\n'
                u'体感温度 : {0[fl]}摄氏度\n'
            ).format(now_weather)
            return weather_report.encode('utf8')


