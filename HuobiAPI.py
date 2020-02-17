#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helper import http_get_request


class HuobiAPI:

	def __init__(self,url,access_key,secret_key):
		self.__url = url
		self.__access_key = access_key
		self.__secret_key = secret_key



	# 获取KLine
	def get_contract_kline(self, symbol, period, size=150):
		"""
		:param symbol  BTC_CW, BTC_NW, BTC_CQ , ...
		:param period: 可选值：{1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
		:param size: [1,2000]
		:return:
		"""
		params = {'symbol': symbol,
				  'period': period}
		if size:
			params['size'] = size
	
		url = self.__url + '/market/history/kline'
		return http_get_request(url, params)




	def get_contract_info(self, symbol='', contract_type='', contract_code=''):
		"""
		参数名称		 参数类型  必填	描述
		symbol		  string  false   "BTC","ETH"...
		contract_type   string  false   合约类型: this_week:当周 next_week:下周 quarter:季度
		contract_code   string  false   BTC181228
		备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
		"""
		params = {}
		if symbol:
			params['symbol'] = symbol
		if contract_type:
			params['contract_type'] = contract_type
		if contract_code:
			params['contract_code'] = contract_code
	
		url = self.__url + '/api/v1/contract_contract_info'
		return http_get_request(url, params)