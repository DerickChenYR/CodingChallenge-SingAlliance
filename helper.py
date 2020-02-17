#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests
import json
from datetime import datetime, timezone

TIMEOUT = 5

def http_get_request(url, params, add_to_headers=None):
	headers = {
		"Content-type": "application/x-www-form-urlencoded",
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
	}
	if add_to_headers:
		headers.update(add_to_headers)
	postdata = urllib.parse.urlencode(params)
	try:
		response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT)
		if response.status_code == 200:
			return response.json()
		else:
			print(response)
			return {"status":"fail"}
	except Exception as e:
		print("httpGet failed, detail is:%s" %e)
		return {"status":"fail","msg": "%s"%e}



#Load API access and secret keys from config
#Returning a tuple
def load_auth_keys():
	try:

		with open("config.json") as secret:

			credentials = json.load(secret)
			Huobi_keys = credentials["API_keys"]["Huobi"]

			return Huobi_keys["access"], Huobi_keys["secret"], Huobi_keys["url"]

	except FileNotFoundError:
		print("Error - config file not found.")



#Load analysis inputs from text file.
#Inputs are to be formatted in 4 lines
	#Start Time - in the format 2019-11-01T05:00:00+00:00
	#End Time - in the format 2019-11-01T05:00:00+00:00
	#Period - {1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
	#Contracts - in a comma separated list of contract codes
	#Contract Type - e.g. quarter
def load_inputs():
	try:
		params = {}
		with open("input.txt") as file:
			inputs = file.read().split("\n")

			#Input format error
			if len(inputs)!=5:
				raise ValueError

			start_date_str = inputs[0]
			end_date_str = inputs[1]

			params["period"] = inputs[2]
			params["contract_type"] = inputs[4].lower()

			time_unit = "".join([i for i in params["period"] if not i.isdigit()])

			params["start_date"], params["end_date"], params["duration"], params["offset"] = parse_input_dates(start_date_str, end_date_str, time_unit)
			
			params["contract_codes"] = inputs[3].replace(" ", "").split(",")
			params["contract_symbols"] = []
			for code in params["contract_codes"]:
				params["contract_symbols"].append("".join(i for i in code if not i.isdigit()))

			return params 

	except FileNotFoundError:
		print("Error - input file not found.")

	except ValueError:
		print("Error - input format invlid.")



#Parse string datetime to date time objs
#Currently supports 60min periods
def parse_input_dates(start_date_str, end_date_str, time_unit):

	time_format = '%Y-%m-%dT%H:%M:%S%z'
	start_date_obj = datetime.strptime(start_date_str, time_format)
	end_date_obj = datetime.strptime(end_date_str, time_format)

	duration = end_date_obj - start_date_obj
	offset = datetime.now(timezone.utc) - end_date_obj

	#TODO: deal with different analysis time periods, e.g. 15min, 1week

	duration_period = duration.days * 24 + duration.seconds//3600
	offset_period = offset.days * 24 + offset.seconds//3600

	if duration_period + offset_period > 2000:
		raise ValueError("Input Error - Analysis timeframe exceeds maximum retrievable historical data from API.")

	return start_date_obj, end_date_obj, duration_period, offset_period