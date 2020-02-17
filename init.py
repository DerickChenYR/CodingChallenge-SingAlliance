
from helper import load_auth_keys, load_inputs
import json
from HuobiAPI import HuobiAPI
from data_etl import load_contract_historical
'''

Reference for Optimization Algo

#https://www.quantopian.com/posts/the-efficient-frontier-markowitz-portfolio-optimization-in-python
#https://www.pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/
'''


inputs = load_inputs()
print(inputs)
print("\n\n\n")

ACCESS_KEY, SECRET_KEY, URL = load_auth_keys()


API = HuobiAPI(URL, ACCESS_KEY, SECRET_KEY)

symbols = inputs["contract_symbols"]

for symbol in symbols:

	load_contract_historical(API, symbol, inputs["duration"], inputs["offset"], inputs["period"], inputs["contract_type"])
	break
