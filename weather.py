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

TIME_BETWEEN_UPDATES = timedelta(seconds=1800)

DEFAULT_TIME = dt_util.now()

CONF_LOCATION = 'location'
CONF_HEFENG_APPKEY = 'hefengkey'
CONF_CAIYUN_APPKEY = 'caiyunkey'

ATTRIBUTION = "来自和风天气的天气数据"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    # vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_LOCATION): cv.string,
    vol.Required(CONF_HEFENG_APPKEY): cv.string,
    vol.Required(CONF_CAIYUN_APPKEY): cv.string,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the hefeng weather."""
    _LOGGER.info("setup platform weather.Heweather...")
    location = config.get(CONF_LOCATION)
    hefengkey = config.get(CONF_HEFENG_APPKEY)
    caiyunkey = config.get(CONF_CAIYUN_APPKEY)    
    data = WeatherData(location,hefengkey,caiyunkey)
    yield from data.async_update(dt_util.now())
    async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)

    async_add_devices([HeFengWeather('my weather',data)], True)


class WeatherData(object):

    @property
    def hefeng(self):
        """Return the name of the sensor."""
        return self._hefeng

    @property
    def caiyun(self):
        """Return the name of the sensor."""
        return self._caiyun

    def __init__(self,location,hefengkey,caiyunkey):
        self._hefeng = hefeng.HeFengWeather(location,hefengkey)
        comps = location.split(',')
        self._caiyun = caiyun.CaiyunWeather(caiyunkey,comps[0],comps[1])

    @asyncio.coroutine
    def async_update(self, now):
        """从远程更新信息."""
        self.hefeng.load()
        self.caiyun.load()
        _LOGGER.info("Update from JingdongWangxiang's OpenAPI...")


class HeFengWeather(WeatherEntity):
    """Representation of a weather condition."""

    def __init__(self, object_id,data):
        """Initialize the  weather."""
        self._temperature = None
        self._humidity = None
        self._wind_bearing = None
        self._wind_speed = None
        self._pressure = None
        self._condition = None

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
        caiyun = self._data.caiyun
        hefeng = self._data.hefeng
        hourlys = []
        for f in hefeng.hourly:
            hourlys.append({
                'date':f.date,
                'condition':f.txt,
                'temperature':f.temperature,
                'probability':f.probability
                })
        dailys = []
        for f in caiyun.daily.forecasts:
            dailys.append({
                'date':f.date,
                'max': f.forecast_max.temperature,
                'min': f.forecast_min.temperature,
                'day': f.skycon_day.txt,
                'night': f.skycon_day.txt,
                })
        return {
            'description':caiyun.forecast_keypoint,
            'minutely_description':caiyun.minutely.description,
            'hourly_description':caiyun.hourly.description,
            'now': {
                'temperature': caiyun.realtime.temperature,
                'condition': caiyun.realtime.skycon.txt,
                'humidity': caiyun.realtime.humidity * 100,
                'aqi': caiyun.realtime.aqi.aqi,
                'pm25': caiyun.realtime.aqi.pm25,
                'wind_direction': caiyun.realtime.wind_direction_description,
                'wind_degree': caiyun.realtime.wind_direction,
                'wind_speed': caiyun.realtime.wind_speed,
                'pressure': caiyun.realtime.pressure / 100

            },
            'hourlys': hourlys,
            'dailys': dailys
        }


    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""
        caiyun = self._data.caiyun
        hefeng = self._data.hefeng
        self._temperature = caiyun.realtime.temperature
        self._humidity = caiyun.realtime.humidity * 100
        self._wind_bearing = caiyun.realtime.wind_direction_description
        self._wind_speed = caiyun.realtime.wind_speed
        self._pressure = caiyun.realtime.pressure / 100
        self._condition = caiyun.realtime.skycon.txt
        _LOGGER.debug('async_update')


