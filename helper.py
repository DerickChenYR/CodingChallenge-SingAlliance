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
			error_message = http_status_handler(response.status_code)
			print(error_message)
			return {"status":"fail","msg":error_message}
	except Exception as e:
		print("httpGet failed, detail is:%s" %e)
		return {"status":"fail","msg": "%s"%e}



#Interprete error message from status code
def http_status_handler(status_code):

	if status_code == 2001:
		return "Invalid authentication."

	elif status_code == 2002:
		return "Authentication required."

	elif status_code == 2003:
		return "Authentication failed."

	elif status_code == 2004:
		return "Number of visits exceeds limit."

	elif status_code == 2005:
		return "Connection has been authenticated."

	elif status_code == 2010:
		return "Topic error."

	elif status_code == 2011:
		return "Contract doesn't exist."

	elif status_code == 2012:
		return "Topic not subscribed."

	elif status_code == 2013:
		return "Authentication type doesn't exist."

	elif status_code == 2014:
		return "Repeated subscription."

	elif status_code == 2030:
		return "Exceeds connection limit of single user."

	elif status_code == 2040:
		return "Missing required parameter."

	else:
		return "Undocumented API response error code!"



#Load API access and secret keys from config
#Returning a tuple
def load_auth_keys():
	try:

		#Loads API credentials from config file
		with open("config.json") as secret:

			credentials = json.load(secret)
			Huobi_keys = credentials["API_keys"]["Huobi"]

			return Huobi_keys["access"], Huobi_keys["secret"], Huobi_keys["url"]

	except FileNotFoundError:
		print("Warning - config file not found. API can only retrieve public data that does not require authentication.")

		return None, None, "https://api.hbdm.com"



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

			if params["period"] != "60min":
				raise ValueError("This script does not currently support time intervals other than 60min.")

			params["contract_type"] = inputs[4].lower()

			time_unit = "".join([i for i in params["period"] if not i.isdigit()])

			params["start_date"], params["end_date"], params["duration"], params["offset"] = parse_input_dates(start_date_str, end_date_str, time_unit)
			
			params["contract_codes"] = inputs[3].upper().replace(" ", "").split(",")
			params["contract_symbols"] = []
			for code in params["contract_codes"]:
				params["contract_symbols"].append("".join(i for i in code if not i.isdigit()))

			return params 

	except FileNotFoundError:
		print("Input Error - input file not found.")

	except ValueError:
		print("Input Error - input format invlid.")



#Parse string datetime to date time objs
#Currently supports 60min periods
def parse_input_dates(start_date_str, end_date_str, time_unit):

	#Parse string date times to datetime objects
	time_format = '%Y-%m-%dT%H:%M:%S%z'
	try:
		start_date_obj = datetime.strptime(start_date_str, time_format)
		end_date_obj = datetime.strptime(end_date_str, time_format)
	except:
		raise ValueError("Input Error - input date/time format invalid.")

	duration = end_date_obj - start_date_obj
	offset = datetime.now(timezone.utc) - end_date_obj

	#TODO: deal with different analysis time periods, e.g. 15min, 1week
	if time_unit != "min":
		raise ValueError("This script does not currently support time intervals other than min.")

	duration_period = duration.days * 24 + duration.seconds//3600
	offset_period = offset.days * 24 + offset.seconds//3600

	if duration_period + offset_period > 2000:
		raise ValueError("Input Error - Analysis timeframe exceeds maximum retrievable historical data from API.")

	return start_date_obj, end_date_obj, duration_period, offset_period



def write_output(output_dir, file_name, data):

    with open(output_dir + "/" + file_name, "w") as file:
        file.write(str(data))
