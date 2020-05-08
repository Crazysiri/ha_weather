import os, io, sys
import requests
import json
import hashlib


"""
每次会缓存一个 originalJson的字段 从服务端拿到的原始json格式的数据 load完可以直接获取
"""
class WeatherReader():

	@property
	def originalJson(self):
		"""Return the attribution."""
		return self._originalJson


	def __init__(self,url,parses,identity = None):
		"""
		identity 存储时用，如果有这个就用这个拼上url last component存储 否则就用url的md5存
		parses 是解析的层级 例如和风 需要解析到 ['result']['HeWeather5']
		"""
		self._url = url

		self._identity = identity

		self._parses = parses

		self.readFromJson()

	def load(self):

		req = requests.get(self._url)

		if req.status_code != 200:
			print('request error')
			pass
		else:
			json_data = req.json()
			self._originalJson = json_data
			for key in self._parses:
				self._originalJson = self._originalJson[key]
			self.saveJsonToDisk(self._originalJson)

	def saveJsonToDisk(self,jsonData):

		name,path = self.name()
		if not os.path.exists(os.path.dirname(path)):
			print('not exists')
			os.mkdir(os.path.dirname(path))
		with open(path,'w') as f:
			json.dump(jsonData,f)

	def name(self):
		if self._identity:
			p,n = os.path.split(self._url)
			name = self._identity + '_' + n
		else:
			md5 = hashlib.md5()
			md5.update(self._url.encode(encoding='utf-8'))
			name = md5.hexdigest()
		path = os.path.dirname(os.path.realpath(__file__)) + '/downloads/' + name + '.json'
		return name,path

	def readFromJson(self):
		name,path = self.name()
		try:
			with open(path,'r') as f:
				self._originalJson = json.load(f)
		except Exception as e:
			print('readFromJsonError:')
			print(e)