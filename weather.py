"""

"""
import logging
from datetime import datetime, timedelta

import asyncio
from homeassistant.helpers.event import async_track_time_interval

import voluptuous as vol

from homeassistant.components.weather import (
    WeatherEntity, ATTR_FORECAST_CONDITION, ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW, ATTR_FORECAST_PRECIPITATION, ATTR_FORECAST_TIME, PLATFORM_SCHEMA)
from homeassistant.const import (ATTR_ATTRIBUTION, TEMP_CELSIUS, CONF_NAME)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util

from . import caiyun
from . import hefeng

_LOGGER = logging.getLogger(__name__)

TIME_BETWEEN_UPDATES = timedelta(seconds=3600)

DEFAULT_TIME = dt_util.now()

CONF_DEVICE_TRACKER_ENTITY = 'device'

CONF_LOCATION = 'location'
CONF_HEFENG_APPKEY = 'hefengkey'
CONF_HEFENG_FREE_APPKEY = 'hefengfreekey'
CONF_CAIYUN_APPKEY = 'caiyunkey'

#一共五个api 分别控制是否是免费
CONF_HEFENG_NOW_IS_FREE = 'free_now'
CONF_HEFENG_DAILY_IS_FREE = 'free_daily'
CONF_HEFENG_HOURLY_IS_FREE = 'free_hourly'
CONF_HEFENG_AIR_IS_FREE = 'free_air'
CONF_HEFENG_LIFESTYLE_IS_FREE = 'free_lifestyle'

ATTRIBUTION = "来自和风天气的天气数据"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_DEVICE_TRACKER_ENTITY,default=''): cv.string,
    vol.Required(CONF_LOCATION): cv.string,
    vol.Optional(CONF_HEFENG_APPKEY,default=''): cv.string,
    vol.Required(CONF_HEFENG_FREE_APPKEY): cv.string,  
    vol.Required(CONF_CAIYUN_APPKEY): cv.string,
    vol.Optional(CONF_HEFENG_NOW_IS_FREE,default=True): cv.boolean,
    vol.Optional(CONF_HEFENG_DAILY_IS_FREE,default=True): cv.boolean,
    vol.Optional(CONF_HEFENG_HOURLY_IS_FREE,default=True): cv.boolean,
    vol.Optional(CONF_HEFENG_AIR_IS_FREE,default=True): cv.boolean,
    vol.Optional(CONF_HEFENG_LIFESTYLE_IS_FREE,default=True): cv.boolean,

})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the hefeng weather."""
    _LOGGER.info("setup platform weather.Heweather...")
    name = config.get(CONF_NAME)
    location = config.get(CONF_LOCATION)
    hefengkey = config.get(CONF_HEFENG_APPKEY)
    hefengfreekey = config.get(CONF_HEFENG_FREE_APPKEY)
    caiyunkey = config.get(CONF_CAIYUN_APPKEY)

    device = config.get(CONF_DEVICE_TRACKER_ENTITY)

    #这里是确定哪些是免费哪些是收费api，默认都是免费即下面的位运算的值都需要 或运算，相关相当于二进制：11111    
    free = 0
    if config.get(CONF_HEFENG_NOW_IS_FREE):
        free = free | hefeng.HEFENG_NOW_IS_FREE
    if config.get(CONF_HEFENG_DAILY_IS_FREE):
        free = free | hefeng.HEFENG_FORECAST_IS_FREE
    if config.get(CONF_HEFENG_HOURLY_IS_FREE):
        free = free | hefeng.HEFENG_HOURLY_IS_FREE      
    if config.get(CONF_HEFENG_AIR_IS_FREE):
        free = free | hefeng.HEFENG_AIR_IS_FREE       
    if config.get(CONF_HEFENG_LIFESTYLE_IS_FREE):
        free = free | hefeng.HEFENG_LIFESTYLE_IS_FREE


    data = WeatherData(location,hefengkey,hefengfreekey,caiyunkey,free)
    yield from data.async_update(dt_util.now())
    async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)

    async_add_devices([HeFengWeather(hass,name,data)], True)

    if device:
        device_data = WeatherData(location,hefengkey,hefengfreekey,caiyunkey,free)
        yield from device_data.async_update(dt_util.now())
        async_track_time_interval(hass, device_data.async_update, TIME_BETWEEN_UPDATES)
        name = '_'.join(device.split('.'))
        async_add_devices([HefengWeatherLocation(hass,name,device_data,device)], True)                



class WeatherData(object):

    @property
    def is_load(self):
        """Return the name of the sensor."""
        return self._is_load    

    @property
    def hefeng(self):
        """Return the name of the sensor."""
        return self._hefeng

    @property
    def caiyun(self):
        """Return the name of the sensor."""
        return self._caiyun

    def __init__(self,location,hefengkey,hefengfreekey,caiyunkey,free):
        self._hefeng = hefeng.HeFengWeather(location,hefengkey,hefengfreekey,free=free)     
        comps = location.split(',')
        self._caiyun = caiyun.CaiyunWeather(caiyunkey,comps[0],comps[1])
        self._is_load = False

    @asyncio.coroutine
    def async_update(self, now):
        """从远程更新信息."""
        self.hefeng.load()
        self.caiyun.load()
        self._is_load = True
        _LOGGER.info("Update from JingdongWangxiang's OpenAPI...")

    @is_load.setter
    def is_load(self,is_load):
        self._is_load = is_load



class HeFengWeather(WeatherEntity):
    """Representation of a weather condition."""

    def __init__(self,hass, object_id,data):
        """Initialize the  weather."""
        self._attributes = None
        self._temperature = None
        self._humidity = None
        self._wind_bearing = None
        self._wind_speed = None
        self._pressure = None
        self._condition = None
        self._hass = hass

        self._object_id = object_id
        self._data = data
        _LOGGER.debug('__init__')

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._object_id

    @property
    def registry_name(self):
        """返回实体的friendly_name属性."""
        return '{} {}'.format('和风天气', self._name)

    @property
    def should_poll(self):
        """attention No polling needed for a demo weather condition."""
        return True

    @property
    def temperature(self):
        """Return the temperature."""
        return self._temperature

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        return self._humidity

    @property
    def wind_bearing(self):
        """Return the wind speed."""
        return self._wind_bearing

    @property
    def wind_speed(self):
        """Return the wind speed."""
        return self._wind_speed

    @property
    def pressure(self):
        """Return the pressure."""
        return self._pressure

    @property
    def condition(self):
        """Return the weather condition."""
        return self._condition

    @property
    def attribution(self):
        """Return the attribution."""
        return 'Powered by Home Assistant'

    @property
    def device_state_attributes(self):
        """设置其它一些属性值."""
        return self._attributes

    def setAttributes(self):
        if not self._data.is_load:
            return
        self._data.is_load = False

        caiyun = self._data.caiyun
        hefeng = self._data.hefeng

        realtime = caiyun.realtime
        if realtime:
            self._temperature = realtime.temperature
            self._humidity = realtime.humidity * 100
            self._wind_bearing = realtime.wind_direction_description
            self._wind_speed = realtime.wind_speed
            self._pressure = realtime.pressure / 100
            self._condition = realtime.skycon.condition

        hourlys = []
        if hefeng.hourly:
            for f in hefeng.hourly:
                is_probability = True
                if f.probability == '0':
                    is_probability = False
                hourlys.append({
                    'date':f.date,
                    'time':f.time,
                    'condition':f.condition,
                    'temperature':f.temperature,
                    'probability':f.probability,
                    'is_probability':is_probability
                    })
        dailys = []
        if caiyun.daily.forecasts:
            for f in caiyun.daily.forecasts:
                dailys.append({
                    'date':f.date,
                    'week_description':f.week_description,
                    'date_description':f.date_description,
                    'max': f.forecast_max.temperature,
                    'min': f.forecast_min.temperature,
                    'day': f.skycon_day.condition,
                    'night': f.skycon_day.condition,
                    })
        self._attributes = {
            'update_time':hefeng._now_reader.originalJson['update']['loc'],
            'description':caiyun.forecast_keypoint,
            'minutely_description':caiyun.minutely.description,
            'hourly_description':caiyun.hourly.description,
            'now': {
                'temperature': caiyun.realtime.temperature,
                'condition': caiyun.realtime.skycon.condition,
                'humidity': caiyun.realtime.humidity * 100,
                'aqi': caiyun.realtime.aqi.aqi,
                'pm25': caiyun.realtime.aqi.pm25,
                'pm10': caiyun.realtime.aqi.pm10,
                'wind_direction': caiyun.realtime.wind_direction_description,
                'wind_degree': caiyun.realtime.wind_direction,
                'wind_speed': caiyun.realtime.wind_speed,
                'pressure': caiyun.realtime.pressure / 100,
                'index': caiyun.realtime.life_comfort_index,
                'comfort': caiyun.realtime.life_comfort_desc,                
                'city': hefeng.now.city,
                'area': hefeng.now.area
            },
            'hourlys': hourlys,
            'dailys': dailys
        }            

    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""        
        self.setAttributes()
        _LOGGER.debug('ha async update')



class HefengWeatherLocation(HeFengWeather):


    def __init__(self,hass, object_id,data,device):
        super(HefengWeatherLocation, self).__init__(hass, object_id,data)
        _LOGGER.info("HefengWeatherLocation init")


    @asyncio.coroutine
    def async_update(self):
        _LOGGER.info("start")
        self.setAttributes()                
        _LOGGER.info("end")

