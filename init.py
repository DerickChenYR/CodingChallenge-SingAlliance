#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helper import load_auth_keys, load_inputs, write_output
import json
from HuobiAPI import HuobiAPI
from data_etl import load_contract_historical, create_portfolio, optimise
import pandas as pd



DEBUG = False    #toggle for more debugging messages
OUTPUT_DIR = './output'   #output directory for graph and optimal weightage output
OUTPUT_FILENAME = 'results.txt'    #filename for optimal weightage output
NUM_SIMS = 25000	#number of simulations of different weightages to run



def main():

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
		try:
			df = load_contract_historical(API, symbol, inputs["duration"], inputs["offset"], inputs["period"], inputs["contract_type"], debug = DEBUG)
			klines.append(df)
		except ValueError:
			print("Error - Failed to load data for {}, excluded from analysis!".format(symbol))

	print("Successfully retrieved symbol historical performance")

	#Create combined portfolio
	print("Creating portfolio and running {} simulations".format(NUM_SIMS))
	portfolio = create_portfolio(klines)
	dict_best = optimise(portfolio, num_sims = NUM_SIMS, debug = DEBUG, output_dir = OUTPUT_DIR).to_dict()

	#Remove data not required for the output
	del dict_best['ret']
	del dict_best['stdev']
	del dict_best['sharpe']

	#Write output
	write_output(OUTPUT_DIR, OUTPUT_FILENAME, dict_best)
	print("Wrote results to {}".format(OUTPUT_DIR + "/" + OUTPUT_FILENAME))
	print("Script Completed")




if __name__ == "__main__":

	main()