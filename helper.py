#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests
import json

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

	with open("config.json") as secret:

		credentials = json.load(secret)
		Huobi_keys = credentials["API_keys"]["Huobi"]

		return Huobi_keys["access"], Huobi_keys["secret"], Huobi_keys["url"]



#Load analysis inputs from text file.
#Inputs are to be formatted in 4 lines
	#Start Time - in the format 2019-11-01T05:00:00+00:00
	#End Time - in the format 2019-11-01T05:00:00+00:00
	#Period - {1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
	#Contracts - in a comma separated list of contract codes
def load_inputs():
	try:
		params = {}
		with open("input.txt") as file:
			inputs = file.read().split("\n")

			#Input format error
			if len(inputs)!=4:
				raise ValueError

			params["start_time"] = inputs[0]
			params["end_time"] = inputs[1]
			params["period"] = inputs[2]
			params["contracts"] = inputs[3].replace(" ", "").split(",")

			return params 
			
	except FileNotFoundError:
		print("Error - input file not found.")

	except ValueError:
		print("Error - input format invlid.")