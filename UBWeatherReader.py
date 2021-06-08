import os, io, sys
import requests
import json
import hashlib


"""
每次会缓存一个 originalJson的字段 从服务端拿到的原始json格式的数据 load完可以直接获取
调用顺序 1.init 2.setURL 3.load 4.originalJson
"""
class WeatherReader():

	@property
	def originalJson(self):
		"""Return the attribution."""
		return self._originalJson


	def __init__(self,parses,savename = None):
		"""
		savename 存储时用，如果有name 就不md5随机值了
		parses 是解析的层级 例如和风 需要解析到 ['result']['HeWeather5']
		"""
		self._savename = savename

		self._parses = parses

		self._originalJson = None

		self._session = requests.session()
		self._session.keep_alive = False

	def setURL(self,url,params):
		self._url = url
		if params == None:
			params = ''
		self._params = params	
		#每次重启没数据的时候加载一次就可以
		if not self._originalJson:	
			self.readFromJson()


	def load(self):
		print(self._url+self._params)
		req = self._session.get(self._url + self._params)
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
		if self._savename:
			name = self._savename
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