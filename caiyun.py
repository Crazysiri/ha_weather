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

	#空气质量相关
	@property
	def aqi(self):
		return self._aqi

	@property
	def aqi_usa(self):
		return self._aqi_usa

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


	@pm25.setter
	def pm25(self,pm25):
		self._pm25 = pm25

	@aqi.setter
	def aqi(self,aqi):
		self._aqi = aqi

	@aqi_usa.setter
	def aqi_usa(self,aqi_usa):
		self._aqi_usa = aqi_usa

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

#天气状态
class Skycon():

	@property
	def skycon(self):
		"""PARTLY_CLOUDY_NIGHT skycon"""
		return self._skycon

	@property
	def condition(self):
		"""天气：sunny skycon"""
		return CONDITION_CLASSES[self.skycon]

	@property
	def txt(self):
		"""天气：晴"""
		return SKYCON_TYPE[self.skycon]

	@skycon.setter
	def skycon(self,skycon):
		self._skycon = skycon


class ForecastDay():

	@property
	def date(self):
		"""日期"""
		return self._date

	@property
	def forecast_max(self):
		"""Forecast class """
		try:
			f = self._forecast_max
		except Exception as e:
			self._forecast_max = Forecast()
		return self._forecast_max

	@property
	def forecast_min(self):
		"""Forecast class"""
		try:
			f = self._forecast_min
		except Exception as e:
			self._forecast_min = Forecast()		
		return self._forecast_min

	@property
	def skycon_day(self):
		"""PARTLY_CLOUDY_NIGHT"""
		try:
			f = self._skycon_day
		except Exception as e:
			self._skycon_day = Skycon()			
		return self._skycon_day	

	@property
	def skycon_night(self):
		"""PARTLY_CLOUDY_NIGHT"""
		try:
			f = self._skycon_night
		except Exception as e:
			self._skycon_night = Skycon()			
		return self._skycon_night

	@property
	def skycon_average(self):
		"""PARTLY_CLOUDY_NIGHT"""
		try:
			f = self._skycon_average
		except Exception as e:
			self._skycon_average = Skycon()			
		return self._skycon_average

	@date.setter
	def date(self,date):
		self._date = date



class Forecast():

	@property
	def date(self):
		"""日期"""
		return self._date			

	@property
	def temperature(self):
		"""温度"""
		return self._temperature

	@property
	def humidity(self):
		"""湿度"""
		return self._humidity	

	@property
	def skycon(self):
		"""PARTLY_CLOUDY_NIGHT"""
		try:
			f = self._skycon
		except Exception as e:
			self._skycon = Skycon()			
		return self._skycon	

	@property
	def condition(self):
		"""天气：sunny skycon"""
		return CONDITION_CLASSES[self.skycon]

	@property
	def txt(self):
		"""天气：晴"""
		return SKYCON_TYPE[self.skycon]

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
	def precipitation(self):
		"""降雨量"""
		return self._precipitation

	@property
	def aqi(self):
		"""Aqi class"""
		try:
			aqi = self._aqi
		except Exception as e:
			self._aqi = Aqi()
		return self._aqi	

	@property
	def life_comfort_index(self):
		"""life_index.comfort.index"""
		return self._life_comfort_index

	@property
	def life_comfort_desc(self):
		"""life_index.comfort.desc"""
		return self._life_comfort_desc



	@temperature.setter
	def temperature(self,temperature):
		self._temperature = temperature

	@date.setter
	def date(self,date):
		self._date = date

	@precipitation.setter
	def precipitation(self,precipitation):
		self._precipitation = precipitation

	@wind_speed.setter
	def wind_speed(self,wind_speed):
		self._wind_speed = wind_speed

	@wind_direction.setter
	def wind_direction(self,wind_direction):
		self._wind_direction = wind_direction

	@humidity.setter
	def humidity(self,humidity):
		self._humidity = humidity

	@pressure.setter
	def pressure(self,pressure):
		self._pressure = pressure


	def __init__(self,obj=None):
		self._obj = obj
		if obj:
			self.parse(obj)
	
	def parse(self,obj):
		# obj = obj['content']
		self._temperature = obj['temperature']
		self._humidity = obj['humidity']
		self.skycon.skycon = obj['skycon']
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
	
	@property
	def forecasts(self):
		"""数组 [Forecast 类]"""
		try:
			f = self._forecasts
		except Exception as e:
			self._forecasts = []
		return self._forecasts

	@property
	def description(self):
		"""未来两小时不会下雨"""
		return self._description


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		#未解析：cloudrate ,pressure ,visibility,dswrf: { "datetime": "2020-05-08T20:00+08:00","value": 0.3} 
		self._description = obj['description']

		count = len(obj['precipitation'])
		for i in range(0,count):
			f = Forecast()
			f.date = obj['precipitation'][i]['datetime']
			f.precipitation = obj['precipitation'][i]['value']
			f.temperature = obj['temperature'][i]['value']
			f.wind_speed = obj['wind'][i]['speed']
			f.wind_direction = obj['wind'][i]['direction']
			f.humidity = obj['humidity'][i]['value']
			f.skycon.skycon = obj['skycon'][i]['value']

			a_dict = obj['air_quality']['aqi'][i]
			f.aqi.aqi = a_dict['value']['chn']
			f.aqi.aqi_usa = a_dict['value']['usa']
			f.aqi.pm25 = obj['air_quality']['pm25'][i]['value']

			self.forecasts.append(f)


"""
Daily 请不要获取 ForcaseDay.forecast_max.skycon相关的 condition txt 因为 这几个值在  skycon_day解析
"""
class Daily():
	#空气质量相关
	@property
	def forecasts(self):
		# ForecastDay class
		return self._forecasts


	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		""" 未解析 astro [{
			"date": "2020-05-08T00:00+08:00",
			"sunrise": {
				"time": "05:06"
			},
			"sunset": {
				"time": "19:15"
			}
		}]
		precipitation [{
			"date": "2020-05-08T00:00+08:00",
			"max": 1.1384,
			"min": 0.0,
			"avg": 0.0
		}]
		visibility cloudrate dswrf life_index
		"""
		temperatures = obj['temperature']
		winds = obj['wind']
		humiditys = obj['humidity']
		pressures = obj['pressure']
		aqis = obj['air_quality']['aqi']
		pm25s = obj['air_quality']['pm25']
		skycons = obj['skycon']
		skycons_day = obj['skycon_08h_20h']
		skycons_night = obj['skycon_20h_32h']

		count = len(temperatures)
		self._forecasts = []
		for i in range(0,count):
			f = ForecastDay()

			f.date = temperatures[i]['date']

			f.forecast_max.aqi.aqi = aqis[i]['max']['chn']
			f.forecast_max.aqi.aqi_usa = aqis[i]['max']['usa']
			f.forecast_min.aqi.aqi = aqis[i]['min']['chn']
			f.forecast_min.aqi.aqi_usa = aqis[i]['min']['usa']
			f.forecast_max.aqi.pm25 = pm25s[i]['max']
			f.forecast_min.aqi.pm25 = pm25s[i]['min']

			f.forecast_max.temperature = temperatures[i]['max']
			f.forecast_min.temperature = temperatures[i]['min']
			f.forecast_max.wind_speed = winds[i]['max']['speed']
			f.forecast_min.wind_speed = winds[i]['min']['speed']
			f.forecast_max.wind_direction = winds[i]['max']['direction']
			f.forecast_min.wind_direction = winds[i]['min']['direction']
			f.forecast_max.humidity = humiditys[i]['max']
			f.forecast_min.humidity = humiditys[i]['min']
			f.forecast_max.pressure = pressures[i]['max']
			f.forecast_min.pressure = pressures[i]['min']
			
			f.skycon_average.skycon = skycons[i]['value']
			f.skycon_day.skycon = skycons_day[i]['value']
			f.skycon_night.skycon = skycons_night[i]['value']

			self._forecasts.append(f)			

			
class CaiyunWeather():


	@property
	def alerts(self):
		"""数组[Alert class]"""
		return self._alerts

	@property
	def forecast_keypoint(self):
		"""未来两小时不会下雨，放心出门吧"""
		return self._forecast_keypoint

	@property
	def realtime(self):
		"""Forecast class"""
		return self._realtime

	@property
	def minutely(self):
		"""Minutely class"""
		return self._minutely

	@property
	def hourly(self):
		"""Hourly class"""
		return self._hourly

	@property
	def daily(self):
		"""Daily class"""
		return self._daily

	@property
	def reader(self):
		"""Return the attribution."""
		return self._reader

	def setLocation(self,longi,lat):
		self._longitude = longi
		self._latitude = lat


	def __init__(self,token,longi,lat):
		self._alerts = []
		self._base_url = 'https://api.caiyunapp.com/v2.5/' + token
		self.setLocation(longi,lat)

		self._reader = WeatherReader(self.weather_url(),'?alert=true',['result'])

		self.parse()

	def parse(self):
		obj = self._reader.originalJson
		if not obj:
			return

		self._forecast_keypoint = obj['forecast_keypoint'] 
		self._realtime = Forecast(obj['realtime'])
		self._minutely = Minutely(obj['minutely'])
		self._hourly = Hourly(obj['hourly'])
		self._daily = Daily(obj['daily'])
		for content in obj['alert']['content']:
			self._alerts.append(Alert(content))

	def load(self):
		self._reader.load()

	def url(self,t):
		return '%s/%s,%s/%s.json' % (self._base_url,self._longitude,self._latitude,t)

	def weather_url(self):
		return self.url('weather')



# w = CaiyunWeather('NTWrwDpqyurbROHa','116.39722824','39.90960456')
# # w.weather.load()
# print(w.hourly.forecasts[0].aqi.pm25)
# print(w.daily.forecasts[0].date)


