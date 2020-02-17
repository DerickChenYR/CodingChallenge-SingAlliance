#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helper import load_auth_keys, load_inputs, write_output
import json
from HuobiAPI import HuobiAPI
from data_etl import load_contract_historical, create_portfolio, optimise
import pandas as pd



DEBUG = False
OUTPUT_DIR = './output'
OUTPUT_FILENAME = 'results.txt'
NUM_SIMS = 25000

print("Script Started")

#Read inputs from file
inputs = load_inputs()

if DEBUG:
	print("Received Inputs:")
	print(inputs)


#Initiate API
ACCESS_KEY, SECRET_KEY, URL = load_auth_keys()
API = HuobiAPI(URL, ACCESS_KEY, SECRET_KEY)

symbols = inputs["contract_symbols"]


#Retrieve symbol performance
klines = []
for symbol in symbols:

	df = load_contract_historical(API, symbol, inputs["duration"], inputs["offset"], inputs["period"], inputs["contract_type"])
	klines.append(df)

print("Successfully retrieved symbol historical performance")

#Create combined portfolio
print("Creating portfolio and running {} simulations".format(NUM_SIMS))
portfolio = create_portfolio(klines)
dict_best = optimise(portfolio, num_sims = NUM_SIMS).to_dict()

del dict_best['ret']
del dict_best['stdev']
del dict_best['sharpe']

#Write output
write_output(OUTPUT_DIR, OUTPUT_FILENAME, dict_best)
print("Wrote results to {}".format(OUTPUT_DIR + "/" + OUTPUT_FILENAME))