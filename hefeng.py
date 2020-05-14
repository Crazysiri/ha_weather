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
	def type(self):
		return self._type

	@property
	def brf(self):
		return self._brf

	@property
	def txt(self):
		return self._txt
	"""docstring for suggestion"""
	def __init__(self,obj):
		self._type = None
		self._brf = None
		self._txt = None
		self._obj = obj
		self.parse()

	def parse(self):
		self._type = self._obj['type'] 
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
		self._aqi = None
		self._co = None
		self._o3 = None
		self._pm10 = None
		self._pm25 = None
		self._quality = None
		self._so2 = None
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
	def city(self):
		"""北京市"""
		return self._city

	@property
	def area(self):
		"""朝阳区"""
		return self._area
	@property
	def date(self):
		"""更新时间 2010-10-10 13:00 或者 2010-10-10 """
		return self._date

	@property		
	def time(self):
		"""时间部分 13:00"""
		if not self._time:
			self._time = self.date.split(' ')[1]
		return self._time

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

	@property
	def wind_direction_description(self):
		try:
			d = self._wind_direction_description
		except Exception as e:
			direction = self.wind_degree
			if direction > 337.4 or direction < 22.5:
				final_direction = '北风'
			elif direction > 22.4 and direction < 67.5:
				final_direction = '东北风'
			elif direction > 67.4 and direction < 112.5:
				final_direction = '东风'
			elif direction > 112.4 and direction < 157.5:
				final_direction = '东南风'
			elif direction > 157.4 and direction < 202.5:
				final_direction = '南风'
			elif direction > 202.4 and direction < 247.5:
				final_direction = '西南风'
			elif direction > 247.4 and direction < 292.5:
				final_direction = '西风'
			elif direction > 292.4 and direction < 337.5:
				final_direction = '西北风'
			else:
				final_direction = '无数据'
			self._wind_direction_description = final_direction
		return self._wind_direction_description

	#daily bool值 表示 是否是一天的 因为一天的需要解析 最大值和最小值 而 实时的只需要解析一个温度即可
	def __init__(self,obj,daily):
		self._time = None
		self._obj = obj
		self.parse(obj,daily)

	@city.setter
	def city(self,city):
		self._city = city

	@area.setter
	def area(self,area):
		self._area = area

	def parse(self,obj,daily):
		#for hourly or now
		if not daily:
			self._code = obj['cond_code']
			self._txt = obj['cond_txt']
			self._temperature = obj['tmp']
		else:
		#for daily
			self._day_code = obj['cond_code_d']
			self._night_code = obj['cond_code_n']
			self._day_txt = obj['cond_txt_d']
			self._night_txt = obj['cond_txt_n']
			self._max_temperature = obj['tmp_max']
			self._min_temperature = obj['tmp_min']
		#for common
		try:
			self._date = obj['time'] #hourly字段
		except Exception as e:
			pass
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
			self._probability = 0
			
		self._pressure = obj['pres']
		self._wind_degree = obj['wind_deg']
		self._wind_direction = obj['wind_dir']
		self._wind_level = obj['wind_sc']
		self._wind_speed = obj['wind_spd']


free_base_url = 'https://free-api.heweather.net/s6'
base_url = 'https://api.heweather.net/s6'
HEFENG_NOW_IS_FREE = 1 << 4
HEFENG_FORECAST_IS_FREE = 1 << 3
HEFENG_HOURLY_IS_FREE = 1 << 2
HEFENG_LIFESTYLE_IS_FREE = 1 << 1
HEFENG_AIR_IS_FREE = 1

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



#['result']['HeWeather5']
	"""docstring for HeFengWeather 
	 save_name_pre ： 定制化存储的名字，例如a 地点的是home b地点的是office
	 free 位运算 11111 now(16)|forecast(8)|hourly(4)|lifestyle(2)|air(1) """
	def __init__(self,location,appkey,freeappkey,save_name_pre='home',free=HEFENG_NOW_IS_FREE|HEFENG_FORECAST_IS_FREE|HEFENG_HOURLY_IS_FREE|HEFENG_AIR_IS_FREE|HEFENG_LIFESTYLE_IS_FREE):
		self._daily = None
		self._hourly = None
		self._now = None
		self._suggestions = None
		self._aqi = None
		if not location or not appkey:
			print('location or appkey must not be null')
			return
		self._free_aqi_city = 'beijing' #默认为beijing 免费api 只能是类似这样的参数
		self._location = location
		self._appkey = appkey
		self._freeappkey = freeappkey
		self._free = free

		# url = "https://way.jd.com/he/freeweather?city=%s&appkey=%s" % (self._city,self._appkey)
		# self._reader = WeatherReader(url,None,['result','HeWeather6',0])
		self._now_reader = WeatherReader(self.now_url(),None,['HeWeather6',0],save_name_pre + '_hefeng_now')
		self._forecast_reader = WeatherReader(self.forecast_url(),None,['HeWeather6',0],save_name_pre + '_hefeng_daily')
		self._hourly_reader = WeatherReader(self.hourly_url(),None,['HeWeather6',0],save_name_pre + '_hefeng_hourly')
		self._lifestyle_reader = WeatherReader(self.lifestyle_url(),None,['HeWeather6',0],save_name_pre + '_hefeng_lifestyle')
		self._air_reader = WeatherReader(self.air_url(),None,['HeWeather6',0],save_name_pre + '_hefeng_air')
		self.parse()

	#如果使用免费api 必须设置这个 否则报错 默认 'beijing'		
	def set_free_aqi_city(self,city):
		self._free_aqi_city = city
		pass

	def now_url(self):
		if self._free & HEFENG_NOW_IS_FREE:
			return free_base_url + '/weather/now' + '?location=' + self._location + '&key=' + self._freeappkey
		else:
			return base_url + '/weather/now' +  '?location=' + self._location + '&key=' + self._appkey

	def forecast_url(self):
		if self._free & HEFENG_FORECAST_IS_FREE:
			return free_base_url + '/weather/forecast' +  '?location=' + self._location + '&key=' + self._freeappkey
		else:
			return base_url + '/weather/forecast' +  '?location=' + self._location + '&key=' + self._appkey

	def hourly_url(self):
		if self._free & HEFENG_HOURLY_IS_FREE:
			return free_base_url + '/weather/hourly' +  '?location=' + self._location + '&key=' + self._freeappkey
		else:
			return base_url + '/weather/hourly' +  '?location=' + self._location + '&key=' + self._appkey

	def lifestyle_url(self):
		if self._free & HEFENG_LIFESTYLE_IS_FREE:
			return free_base_url + '/weather/lifestyle' +  '?location=' + self._location + '&key=' + self._freeappkey
		else:
			return base_url + '/weather/lifestyle' +  '?location=' + self._location + '&key=' + self._appkey

	def air_url(self):
		if self._free & HEFENG_AIR_IS_FREE:
			print('如果使用免费api 必须设置这个 否则报错 默认 beijing')
			return free_base_url + '/air/now' + '?location=' + self._free_aqi_city + '&key=' + self._freeappkey
		else:
			return base_url + '/air/now' +  '?location=' + self._location + '&key=' + self._appkey

	def load(self):
		self._now_reader.load()
		self._forecast_reader.load()
		# self._hourly_reader.load()
		self._lifestyle_reader.load()
		self._air_reader.load()
		self.parse()

	def parse(self):
		if self._air_reader.originalJson:
			obj = self._air_reader.originalJson['air_now_city']
			self._aqi = Aqi(obj)
		if self._forecast_reader.originalJson:
			self._daily = []
			for item in self._forecast_reader.originalJson['daily_forecast']:
				self._daily.append(Forecast(item,True))
		if self._hourly_reader.originalJson:
			self._hourly = []
			for item in self._hourly_reader.originalJson['hourly']:
				self._hourly.append(Forecast(item,False))	
		if self._lifestyle_reader.originalJson:
			self._suggestions = []
			for item in self._lifestyle_reader.originalJson['lifestyle']:
				self._suggestions.append(Suggestion(item))
		if self._now_reader.originalJson:
			self._now = Forecast(self._now_reader.originalJson['now'],False)
			self._now.city = self._now_reader.originalJson['basic']['parent_city']
			self._now.area = self._now_reader.originalJson['basic']['location']

# print(obj.hourly[0].temperature)
# obj.load()
# print(obj.hourly[0])
# print(obj.suggestions[0].description)
