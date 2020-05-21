#!/usr/local/bin/python3
# coding=utf-8


import os, io, sys
import json

# from datetime import timedelta
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import  UBWeatherReader
from UBWeatherReader import WeatherReader

#https://open.caiyunapp.com/通用预报接口/v2.5#.E5.A4.A9.E6.B0.94.E7.8E.B0.E8.B1.A1.E4.BB.A3.E7.A0.81
CONDITION_CLASSES = {
    'CLEAR_DAY':'sunny', #晴（白天）
    'CLEAR_NIGHT':'sunny_night',#晴 （夜间）
    'PARTLY_CLOUDY_DAY':'partlycloudy', #多云
    'PARTLY_CLOUDY_NIGHT':'partlycloudy_night',#多云
    'CLOUDY':'cloudy', #阴
    'LIGHT_HAZE':'fog',#轻度雾霾
    'MODERATE_HAZE':'fog',#中度雾霾
    'HEAVY_HAZE':'fog',#重度雾霾
    'LIGHT_RAIN':'rainy', #小雨    
    'MODERATE_RAIN':'rainy',#中雨
    'HEAVY_RAIN':'rainy',#大雨
    'STORM_RAIN':'pouring',#暴雨
    'FOG':'fog',#雾    
    'LIGHT_SNOW':'snowy',#小雪
    'MODERATE_SNOW':'snowy',#中雪
    'HEAVY_SNOW':'snowy',#大雪
    'STORM_SNOW':'snowy',#暴雪
    'DUST':'fog', #浮尘
    'SAND':'fog',#沙尘
     'WIND':'windy',#大风
}

SKYCON_TYPE = {
    'CLEAR_DAY':'晴天', #晴（白天）
    'CLEAR_NIGHT':'晴夜',#晴 （夜间）
    'PARTLY_CLOUDY_DAY':'多云', #多云
    'PARTLY_CLOUDY_NIGHT':'多云',#多云
    'CLOUDY':'阴', #阴
    'LIGHT_HAZE':'轻度雾霾',#轻度雾霾
    'MODERATE_HAZE':'中度雾霾',#中度雾霾
    'HEAVY_HAZE':'重度雾霾',#重度雾霾
    'LIGHT_RAIN':'小雨', #小雨    
    'MODERATE_RAIN':'中雨',#中雨
    'HEAVY_RAIN':'大雨',#大雨
    'STORM_RAIN':'暴雨',#暴雨
    'FOG':'雾',#雾    
    'LIGHT_SNOW':'小雪',#小雪
    'MODERATE_SNOW':'中雪',#中雪
    'HEAVY_SNOW':'大雪',#大雪
    'STORM_SNOW':'暴雪',#暴雪
    'DUST':'浮尘', #浮尘
    'SAND':'沙尘',#沙尘
     'WIND':'大风',#大风
}

WEEK_TYPE = [
	'周一','周二','周三','周四','周五','周六','周日'
]

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
		self._aqi = 0
		self._aqi_usa = 0
		self._co = 0
		self._o3 = 0
		self._pm10 = 0
		self._pm25 = 0				
		self._quality = ''
		self._quality_usa = ''
		self._so2 = 0		
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

	def __init__(self,obj=None):
		self._obj = obj
		if obj:
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

	def	__init__(self):
		self._skycon = 'CLEAR_DAY'


import datetime
from datetime import timedelta,datetime 

class ForecastDay():

	@property
	def week_description(self):
		"""日期 解析出来的 如果是今天 就是今天，其它就是周一"""
		return self._week_description


	@property
	def date_description(self):
		"""日期 解析出来的 如果跨年就是2000.01.01，其它就是01.29类似"""
		return self._date_description

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

	def	__init__(self):
		self._date_description = None
		self._week_description = None

	@date.setter
	def date(self,date):
		self._date = date
		time = datetime.strptime(date,'%Y-%m-%dT%H:%M%z')
		now = datetime.utcnow() + timedelta(hours=8)	#服务器获取的时间 需要加8小时 	
		if time.year == now.year and time.month == now.month and time.day == now.day:
			self._week_description = '今天'	
		else:
			self._week_description = WEEK_TYPE[time.weekday()]
		if time.year != now.year:
			self._date_description = '%s-%s-%s' % (time.year,time.month,time.day)
		else:
			self._date_description = '%s-%s' % (time.month,time.day)


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
	def wind_level(self):
		"""风力等级 1"""
		if not self._wind_level:
			speed = self.wind_speed
			if speed:
				if speed < 1:
					level = 0
				elif speed <= 5:
					level = 1
				elif speed <= 11:
					level = 2
				elif speed <= 19:
					level = 3
				elif speed <= 28:
					level = 4
				elif speed <= 38:
					level = 5				
				elif speed <= 49:
					level = 6
				elif speed <= 61:
					level = 7
				elif speed <= 74:
					level = 8
				elif speed <= 88:
					level = 9
				elif speed <= 102:
					level = 10
				elif speed <= 117:
					level = 11
				elif speed <= 133:
					level = 12				
				elif speed <= 149:
					level = 13
				elif speed <= 166:
					level = 14
				elif speed <= 183:
					level = 15				
				elif speed <= 201:
					level = 16
				elif speed <= 220:
					level = 17
				self._wind_level = level																
		return self._wind_level

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
		return self._aqi	

	@property
	def life_comfort_index(self):
		"""life_index.comfort.index"""
		return self._life_comfort_index

	@property
	def life_comfort_desc(self):
		"""life_index.comfort.desc"""
		return self._life_comfort_desc

	@property
	def wind_direction_description(self):
		if not self._wind_direction_description:
			direction = self.wind_direction
			if direction:
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
		self._wind_direction = None
		self._wind_speed = None
		self._wind_direction_description = None
		self._wind_level = None
		self._date = ''			
		self._temperature = 0
		self._humidity = 0	
		self._skycon = Skycon()
		self._pressure = 0
		self._precipitation = 0
		self._aqi  = Aqi()	
		self._life_comfort_index = 0
		self._life_comfort_desc	= ''	
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


	def __init__(self,obj=None):
		self._precipitation_2h = []
		self._precipitation = []
		self._probability = []
		self._description = ''

		self._obj = obj
		if obj:
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
		return self._forecasts

	@property
	def description(self):
		"""未来两小时不会下雨"""
		return self._description


	def __init__(self,obj=None):
		self._description = ''
		self._forecasts = []
		self._obj = obj
		if obj:
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


	def __init__(self,obj=None):
		self._forecasts = []
		self._obj = obj
		if obj:
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



	def __init__(self,token,location,save_name_pre='home'):
		self._realtime = Forecast()
		self._location = ''
		self._minutely = Minutely()
		self._hourly = Hourly()
		self._daily = Daily()
		self._reader = None
		self._forecast_keypoint = ''
		self._alerts = []
		self._base_url = 'https://api.caiyunapp.com/v2.5/' + token

		self._reader = WeatherReader(['result'],save_name_pre + '_caiyun_weather')
		self.setLocation(location)
		self.parse()

	def parse(self):
		obj = self._reader.originalJson
		if obj:
			self._forecast_keypoint = obj['forecast_keypoint'] 
			self._realtime = Forecast(obj['realtime'])
			self._minutely = Minutely(obj['minutely'])
			self._hourly = Hourly(obj['hourly'])
			self._daily = Daily(obj['daily'])
			self._alerts = []
			for content in obj['alert']['content']:
				self._alerts.append(Alert(content))


	def setLocation(self,location):
		if self._location != location:
			self._location = location
			self._reader.setURL(self.weather_url(),'?alert=true&dailysteps=7')

	def load(self):
		self._reader.load()
		self.parse()

	def url(self,t):
		return '%s/%s/%s.json' % (self._base_url,self._location,t)

	def weather_url(self):
		return self.url('weather')

# print(WEEK_TYPE[datetime.now().weekday()])

# w = 
# w.load()
# print(w.hourly.forecasts[0].aqi.pm25)
# print(w.daily.forecasts[0].date)


