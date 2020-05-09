#!/usr/local/bin/python3
# coding=utf-8


import os, io, sys
import json

# from datetime import timedelta
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import  UBWeatherReader
from UBWeatherReader import WeatherReader

CONDITION_CLASSES = {
    'CLEAR_DAY':'sunny',
    'CLEAR_NIGHT':'sunny',
    'PARTLY_CLOUDY_DAY':'partlycloudy',
    'PARTLY_CLOUDY_NIGHT':'partlycloudy',
    'CLOUDY':'cloudy',
    'RAIN':'rainy',
    'SNOW':'snowy',
    'WIND':'windy',
    'FOG':'fog',
    'HAZE':'fog',

}

SKYCON_TYPE = {
    'CLEAR_DAY':'晴天',
    'CLEAR_NIGHT':'晴夜',
    'PARTLY_CLOUDY_DAY':'多云',
    'PARTLY_CLOUDY_NIGHT':'多云',
    'CLOUDY':'阴',
    'RAIN':'雨',
    'SNOW':'雪',
    'WIND':'风',
    'FOG':'雾',
    'HAZE':'雾霾',
}

class Aqi():

	@property
	def datetime(self):
		"""hourly里需要"""
		return self._datetime	

	#空气质量相关
	@property
	def aqi(self):
		return self._aqi

	@property
	def aqi_usa(self):
		return self._aqi_usa

	@property
	def aqi(self):
		return self._aqi


	@property
	def co(self):
		return self._co

	@property
	def o3(self):
		return self._o3

	@property
	def pm10(self):
		return self._pm10

	@property
	def pm25(self):
		return self._pm25				

	@property
	def quality(self):
		#文字描述 良好
		return self._quality

	@property
	def quality_usa(self):
		#文字描述 良好
		return self._quality_usa

	@property
	def so2(self):
		return self._so2

	def __init__(self,obj=None):
		self._obj = obj
		if obj:
			self.parse(obj)
	
	def parse(self,obj):
		# [aqi][usa] [description][usa] 美国标准
		self._aqi = obj['aqi']['chn']
		self._aqi_usa = obj['aqi']['usa']
		self._quality_usa = obj['description']['usa'] 
		self._co = obj['co']
		self._o3 = obj['o3']
		self._pm10 = obj['pm10']
		self._pm25 = obj['pm25']
		self._quality = obj['description']['chn'] 
		self._so2 = obj['so2']		
		pass

#预警
class Alert():

	@property
	def status(self):
		"""状态 预警中"""
		return self._status	

	@property
	def location(self):
		"""北京市"""
		return self._location	

	@property
	def source(self):
		"""国家预警发布中心"""
		return self._source

	@property
	def title(self):
		"""雷电预警"""
		return self._title

	@property
	def description(self):
		"""将于xx年发布雷电黄色预警，注意防范！"""
		return self._description	

	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		# obj = obj['content']
		self._status = obj['status']
		self._location = obj['location']
		self._source = obj['source']
		self._title = obj['title']
		self._description = obj['description']	
		pass	

class Forecast():

	@property
	def temperature(self):
		"""温度"""
		return self._temperature

	@property
	def humidity(self):
		"""湿度"""
		return self._humidity	

	@property
	def condition(self):
		"""天气：sunny skycon"""
		return self._condition

	@property
	def txt(self):
		"""天气：晴"""
		return self._txt

	@property
	def wind_speed(self):
		"""风速"""
		return self._wind_speed

	@property
	def wind_direction(self):
		"""风向 360度"""
		return self._wind_direction	

	@property
	def pressure(self):
		"""气压"""
		return self._pressure


	@property
	def aqi(self):
		"""Aqi class"""
		return self._aqi	

	@property
	def life_comfort_index(self):
		"""life_index.comfort.index"""
		return self._life_comfort_index

	@property
	def life_comfort_desc(self):
		"""life_index.comfort.desc"""
		return self._life_comfort_desc


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		# obj = obj['content']
		self._temperature = obj['temperature']
		self._humidity = obj['humidity']
		self._condition = CONDITION_CLASSES[obj['skycon']]
		self._txt = SKYCON_TYPE[obj['skycon']]
		self._wind_speed = obj['wind']['speed']
		self._wind_direction = obj['wind']['direction']
		self._pressure = obj['pressure']
		self._aqi = Aqi(obj['air_quality'])
		self._life_comfort_index = obj['life_index']['comfort']['index']
		self._life_comfort_desc = obj['life_index']['comfort']['desc']



class Minutely():
	#空气质量相关
	@property
	def precipitation_2h(self):
		"""数组 [0,0,0,0]"""
		return self._precipitation_2h

	@property
	def precipitation(self):
		"""数组 [0,0,0,0]"""
		return self._precipitation

	@property
	def probability(self):
		"""数组 [0,0,0,0]"""
		return self._probability

	@property
	def description(self):
		"""未来两小时不会下雨"""
		return self._description


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		# self._precipitation_2h = obj['precipitation_2h']
		# self._precipitation = obj['precipitation']
		self._probability = obj['probability']
		self._description = obj['description']	
		pass

class Hourly():
	#空气质量相关
	@property
	def temperature(self):
		"""数组 [{"datetime": "2020-05-08T20:00+08:00","value": 0.0}]"""
		return self._temperature

	@property
	def precipitation(self):
		"""数组 [{"datetime": "2020-05-08T20:00+08:00","value": 0.0}]"""
		return self._precipitation

	@property
	def humidity(self):
		"""数组 [{"datetime": "2020-05-08T20:00+08:00","value": 0.0}]"""
		return self._humidity	

	@property
	def skycon(self):
		"""数组 [{"datetime": "2020-05-08T20:00+08:00","value": PARTLY_CLOUDY_NIGHT}]"""
		return self._skycon	

	@property
	def wind(self):
		"""数组 ["datetime": "2020-05-08T20:00+08:00","speed": 7.56,"direction": 151.0]"""
		return self._wind

	@property
	def air_quality(self):
		"""数组 [Aqi (只有aqi aqi_usa pm25 datetime字段)]"""
		return self._air_quality

	@property
	def description(self):
		"""未来两小时不会下雨"""
		return self._description


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		self._temperature = obj['temperature']
		self._precipitation = obj['precipitation']
		self._humidity = obj['humidity']
		self._skycon = obj['skycon']	
		self._wind = obj['wind']
		self._air_quality = []
		self._description = obj['description']
		count = len(obj['air_quality']['aqi'])
		for i in range(0,count):
			aqi = obj['air_quality']['aqi'][i]
			pm25 = obj['air_quality']['pm25'][i]['value']
			aqiObj = Aqi()
			aqiObj.aqi = aqi['value']['chn']
			aqiObj.aqi_usa = aqi['value']['usa']
			aqiObj.datetime = aqi['datetime']
			aqiObj.pm25 = pm25
			self._air_quality.append(aqiObj)


class Daily():
	#空气质量相关
	@property
	def temperature(self):
		"""数组 [{
			"date": "2020-05-08T00:00+08:00",
			"max": 17.0,
			"min": 12.87,
			"avg": 12.98
		}]"""
		return self._temperature

	@property
	def wind(self):
		"""数组 [{
			"date": "2020-05-08T00:00+08:00",
			"max": {
				"speed": 11.57,
				"direction": 88.54
			},
			"min": {
				"speed": 4.93,
				"direction": 89.31
			},
			"avg": {
				"speed": 8.76,
				"direction": 99.21
			}
		}]"""
		return self._wind

	@property
	def humidity(self):
		"""数组 [{
			"date": "2020-05-08T00:00+08:00",
			"max": 0.86,
			"min": 0.75,
			"avg": 0.76
		}]"""
		return self._humidity

	@property
	def pressure(self):
		"""[{
			"date": "2020-05-08T00:00+08:00",
			"max": 100601.05,
			"min": 100441.05,
			"avg": 100572.11
		}]"""
		return self._pressure


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		# self._precipitation_2h = obj['precipitation_2h']
		# self._precipitation = obj['precipitation']
		self._probability = obj['probability']
		self._description = obj['description']				

			
class CaiyunWeather():



	@property
	def weather_reader(self):
		"""Return the attribution."""
		return self._weather_reader

	def setLocation(self,longi,lat):
		self._longitude = longi
		self._latitude = lat


	def __init__(self,token,longi,lat):
		self._base_url = 'https://api.caiyunapp.com/v2.5/' + token
		self.setLocation(longi,lat)

		self._weather_reader = WeatherReader(self.weather_url(),'?alert=true',['result'])


	def url(self,t):
		return '%s/%s,%s/%s.json' % (self._base_url,self._longitude,self._latitude,t)

	def weather_url(self):
		return self.url('weather')

	def realtime_url(self):
		return self.url('realtime')

	def minutely_url(self):
		return self.url('minutely')

	def hourly_url(self):
		return self.url('hourly')

	def daily_url(self):
		return self.url('daily')



w = CaiyunWeather('NTWrwDpqyurbROHa','116.39722824','39.90960456')
w.weather_reader.load()


