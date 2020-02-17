#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd



def load_contract_historical(API, contract_symbol, duration, offset, period, contract_type):

	data_head = duration + offset

	if contract_type == "quarter":
		contract_symbol += "_CQ"
	else:
		raise("Error - Unsupported contract type!")

	response = API.get_contract_kline(contract_symbol, period, size = data_head)
	df = pd.DataFrame(response['data'][:duration])
	print(df)