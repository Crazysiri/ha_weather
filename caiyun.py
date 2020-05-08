#!/usr/local/bin/python3
# coding=utf-8


import os, io, sys
import json

# from datetime import timedelta
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import  UBWeatherReader
from UBWeatherReader import WeatherReader

class Aqi():
	#空气质量相关
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
	def so2(self):
		return self._so2

	def __init__(self,obj):
		self._obj = obj
		self.parse(obj)
	
	def parse(self,obj):
		# [aqi][usa] [description][usa] 美国标准
		self._aqi = obj['aqi']['chn']
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
		return self._lhumidity	

	@property
	def condition(self):
		"""天气：晴 skycon"""
		return self._condition

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
	def humidity(self):
		"""湿度"""
		return self._lhumidity	

	@property
	def condition(self):
		"""天气：晴 skycon"""
		return self._condition

	@property
	def wind_speed(self):
		"""风速"""
		return self._wind_speed

	@property
	def wind_direction(self):
		"""风向 360度"""
		return self._wind_direction	



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


