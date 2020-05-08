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
    'sunny': ["晴"],
    'cloudy': ["多云"],
    'partlycloudy': ["少云", "晴间多云", "阴"],
    'windy': ["有风", "微风", "和风", "清风"],
    'windy-variant': ["强风", "疾风", "大风", "烈风"],
    'hurricane': ["飓风", "龙卷风", "热带风暴", "狂暴风", "风暴"],
    'rainy': ["雨","毛毛雨", "小雨", "中雨", "大雨", "阵雨", "极端降雨"],
    'pouring': ["暴雨", "大暴雨", "特大暴雨", "强阵雨"],
    'lightning-rainy': ["雷阵雨", "强雷阵雨"],
    'fog': ["雾", "薄雾","霾"],
    'hail': ["雷阵雨伴有冰雹"],
    'snowy': ["雪","小雪", "中雪", "大雪", "暴雪", "阵雪"],
    'snowy-rainy': ["雨夹雪", "雨雪天气", "阵雨夹雪"],
}

TRANSLATE_SUGGESTION = {
    'air': '空气污染扩散条件指数',
    'drsg': '穿衣指数',
    'uv': '紫外线指数',
    'comf': '舒适度指数',
    'flu': '感冒指数',
    'sport': '运动指数',
    'trav': '旅游指数',
    'cw': '洗车指数',
}


class Suggestion():

	@property
	def description(self):
		#说明
		return TRANSLATE_SUGGESTION[self._key]

	@property
	def key(self):
		return self._key

	@property
	def brf(self):
		return self._brf

	@property
	def txt(self):
		return self._txt
	"""docstring for suggestion"""
	def __init__(self,key,obj):
		self._key = key
		self._obj = obj
		self.parse()

	def parse(self):
		self._brf = self._obj['brf']
		self._txt = self._obj['txt']



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
		self.parse()
	
	def parse(self):
		self._aqi = self._obj['aqi']
		self._co = self._obj['co']
		self._o3 = self._obj['o3']
		self._pm10 = self._obj['pm10']
		self._pm25 = self._obj['pm25']
		self._quality = self._obj['qlty'] 
		self._so2 = self._obj['so2']		
		pass

class Forecast():

#表示实时的时候用这几个
	@property
	def condition(self):
	    """Return the weather condition."""
	    condition = 'unknown'
	    try:
	        condition = [k for k, v in CONDITION_CLASSES.items() if self._txt in v][0]
	    except Exception as e:
	        pass
	    return condition

	@property
	def code(self):
		""" 302 """
		return self._code

	@property
	def txt(self):
		""" 晴 """
		return self._txt

	@property
	def temperature(self):
		return self._temperature

#表示一天的时候用这几个
	@property
	def day_condition(self):
	    """Return the weather condition."""
	    condition = 'unknown'
	    try:
	        condition = [k for k, v in CONDITION_CLASSES.items() if self._day_txt in v][0]
	    except Exception as e:
	        pass
	    return condition

	@property
	def day_condition(self):
	    """Return the weather condition."""
	    condition = 'unknown'
	    try:
	        condition = [k for k, v in CONDITION_CLASSES.items() if self._night_txt in v][0]
	    except Exception as e:
	        pass
	    return condition

	@property
	def day_code(self):
		""" 302 """
		return self._day_code

	@property
	def night_code(self):
		""" 302 """
		return self._night_code

	@property
	def day_txt(self):
		""" 晴 """
		return self._day_txt

	@property
	def night_txt(self):
		""" 晴 """	
		return self._night_txt	

	@property
	def max_temperature(self):
		return self._max_temperature

	@property
	def min_temperature(self):
		return self._min_temperature	

#common 一般的属性

	@property
	def date(self):
		"""更新时间 2010-10-10 """
		return self._date

	@property
	def humidity(self):
		return self._humidity			

	@property
	def possible_precipitation(self):
		""" 可能的降水量 mm """
		return self._possible_precipitation

	@property
	def probability(self):
		""" 可能的概率 """
		return self._probability

	@property
	def pressure(self):
		"""大气压"""
		return self._pressure		

	@property
	def wind_degree(self):
		""" 360度 """
		return self._wind_degree

	@property
	def wind_direction(self):
		""" 风向 """
		return self._wind_direction

	@property
	def wind_level(self):
		""" 风力 """
		return self._wind_level		

	@property
	def wind_speed(self):
		""" 风速 """
		return self._wind_speed

	#daily bool值 表示 是否是一天的 因为一天的需要解析 最大值和最小值 而 实时的只需要解析一个温度即可
	def __init__(self,obj,daily):
		self._obj = obj
		self.parse(obj,daily)

	def parse(self,obj,daily):
		#for houly or now
		if not daily:
			self._code = obj['cond']['code']
			self._txt = obj['cond']['txt']
			self._temperature = obj['tmp']
		else:
		#for daily
			self._day_code = obj['cond']['code_d']
			self._night_code = obj['cond']['code_n']
			self._day_txt = obj['cond']['txt_d']
			self._night_txt = obj['cond']['txt_n']
			self._max_temperature = obj['tmp']['max']
			self._min_temperature = obj['tmp']['min']
		#for common
		try:
			self._date = obj['date']
		except Exception as e:
			pass
		self._humidity = obj['hum']
		try:
			self._possible_precipitation = obj['pcpn']
		except Exception as e:
			self._possible_precipitation = 0
		try:
			self._probability = obj['pop']
		except Exception as e:
			pass
		self._pressure = obj['pres']
		self._wind_degree = obj['wind']['deg']
		self._wind_direction = obj['wind']['dir']
		self._wind_level = obj['wind']['sc']
		self._wind_speed = obj['wind']['spd']


class HeFengWeather():

#每日数据
	@property
	def aqi(self):
		"""Return the Aqi."""
		return self._aqi	

	@property
	def daily(self):
		"""几天的预报，返回数组 里面是forecast 类"""
		return self._daily	

	@property
	def hourly(self):
		"""几小时的预报，返回数组 里面是forecast 类"""
		return self._hourly	

	@property
	def now(self):
		"""当前天气 返回forecast 类"""
		return self._now	
	@property
	def suggestions(self):
		"""建议，返回数组 里面是suggestion 类"""
		return self._suggestions


	@property
	def reader(self):
		"""Return the attribution."""
		return self._reader

#['result']['HeWeather5']
	"""docstring for HeFengWeather"""
	def __init__(self,city,appkey):
		if not city or not appkey:
			print('city or appkey must not be null')
			return
		self._city = city
		self._appkey = appkey
		url = "https://way.jd.com/he/freeweather?city=%s&appkey=%s" % (self._city,self._appkey)
		self._reader = WeatherReader(url,None,['result','HeWeather5',0])
		if self.reader.originalJson:
			self.parse()

	def parse(self):
		obj = self.reader.originalJson['aqi']['city']
		self._aqi = Aqi(obj)
		self._daily = []
		for item in self.reader.originalJson['daily_forecast']:
			self._daily.append(Forecast(item,True))
		self._hourly = []
		for item in self.reader.originalJson['hourly_forecast']:
			self._daily.append(Forecast(item,False))		
		self._suggestions = []
		ss = self.reader.originalJson['suggestion']
		for key in ss:
			self._suggestions.append(Suggestion(key,ss[key]))

		self._now = Forecast(self.reader.originalJson['now'],False)


obj = HeFengWeather('CN101011100','57f99766cf80f29d6b044fe3ed79845b')
# obj.reader.load()
print(obj.now.condition)
print(obj.suggestions[0].description)
