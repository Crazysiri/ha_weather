#!/usr/local/bin/python3
# coding=utf-8


import os, io, sys, re, time, datetime, base64
# from datetime import timedelta
# path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(path)
# import  term
# from term import jieqi

class HeFengWeather(object):


	"""docstring for HeFengWeather"""
	def __init__(self,city,appkey):
		super(HeFengWeather, self).__init__()
		if not city or not appkey:
			print('city or appkey must not be null')
			return
		self.city = city
		self.appkey = appkey

	def load(self):
		
		pass
