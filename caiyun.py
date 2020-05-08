#!/usr/local/bin/python3
# coding=utf-8


import os, io, sys
import json

# from datetime import timedelta
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import  UBWeatherReader
from UBWeatherReader import WeatherReader

class CaiyunWeather():

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
		self._weather_reader = WeatherReader(self.weather_url(),[])


w = CaiyunWeather('NTWrwDpqyurbROHa','116.39722824','39.90960456')
w.weather_reader.load()


