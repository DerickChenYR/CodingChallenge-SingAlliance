from HuobiAPI import HuobiAPI
from helper import load_auth_keys, load_inputs
import json

'''

Reference for Optimization Algo

#https://www.quantopian.com/posts/the-efficient-frontier-markowitz-portfolio-optimization-in-python
#https://www.pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/
'''


inputs = load_inputs()
print(inputs)

ACCESS_KEY, SECRET_KEY, URL = load_auth_keys()

API = HuobiAPI(URL, ACCESS_KEY, SECRET_KEY)

contracts = inputs["contracts"]

for contract in contracts:

	response = API.get_contract_info(contract_code = contract)
	print(response)
