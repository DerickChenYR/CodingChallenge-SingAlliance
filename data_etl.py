#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Retrieve the appropriate historical data for the current symbol from HuobiAPI
def load_contract_historical(API, contract_symbol, duration, offset, period, contract_type, debug = False):

	data_head = duration + offset + 1

	if contract_type == "quarter":
		#Postfix for data type determination
		contract_symbol += "_CQ"
	else:
		raise("Error - Unsupported contract type!")

	#Make API call
	response = API.get_contract_kline(contract_symbol, period, size = data_head)
	
	if debug:
		print("API request for {} returns {}".format(contract_symbol, response['status']))

	#API responds with 200
	if response['status'] == "ok":
		df = pd.DataFrame(response['data'][:duration+1])
	else:
		#Return Error status
		print("API request for {} returns {}, with message {}".format(contract_symbol, response['status'], response['msg']))
		return response

	if df.empty:
		raise ValueError("API call was successful but returned no data")

	#Use the closing price column, replace column name with the current symbol
	new_columns = df.columns.values
	new_columns[1] = contract_symbol
	
	return df[contract_symbol]



#Concatenate individual crypto data series into a portfolio df
#Reference: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
def create_portfolio(list_dfs):

	df = pd.concat(list_dfs, axis=1, sort = False)
	return df



#Return a randomly generated n weights that sum to 1.00
def generate_rand_weights(num):
	weights = np.random.random(num)
	weights /= np.sum(weights)
	return weights



#Compute the returns and std devs for plotting
'''
Reference for Optimization Algo

#https://www.quantopian.com/posts/the-efficient-frontier-markowitz-portfolio-optimization-in-python
#https://www.pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/
'''
def optimise(data_df, num_sims = 25000, debug = False, output_dir = "."):

	num_crypto = len(data_df.columns)
	length_data = len(data_df.index)

	if debug:
		print("Begins optimisation with {} cryptos and {} datapoints".format(num_crypto, length_data))

	#Compute percentage change from adj	
	returns = data_df.pct_change()

	#Compute mean hourly returns and covariance matrix
	mean_hourly_returns = returns.mean()
	cov_matrix = returns.cov()
	

	#Holds the simulated returns, std dev, sharpe ratio and weightages for each crypto
	results = np.zeros((3+ num_crypto, num_sims))

	for i in range(num_sims):

		#Generate random weights for simulation
		weights = generate_rand_weights(num_crypto)

		portfolio_return = np.sum(mean_hourly_returns * weights) * length_data
		portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(length_data)

		#Store results in results array
		results[0,i] = portfolio_return
		results[1,i] = portfolio_std_dev
		#Store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
		results[2,i] = results[0,i] / results[1,i]
		#Record current weights used in the simulation
		for j in range(len(weights)):
			results[j+3,i] = weights[j]



	#Convert results array to Pandas DataFrame
	new_cols = ['ret','stdev','sharpe'] + list(data_df.columns)
	results_frame = pd.DataFrame(results.T, columns=new_cols)


	#Locate position of portfolio with highest Sharpe Ratio
	max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
	#Locate positon of portfolio with minimum standard deviation
	min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

	#print(max_sharpe_port)
	#print(min_vol_port)


	#Create scatter plot coloured by Sharpe Ratio
	fig = plt.figure()
	plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
	plt.xlabel('Volatility')
	plt.ylabel('Returns')
	plt.colorbar()
	plt.plot()
	fig.suptitle(f'Mean-Variance Optimisation with {list(data_df.columns)}', fontsize=8)
	fig.savefig(output_dir + '/graph.png')
	print("Wrote graph to {}".format(output_dir + "/" + 'graph.png'))

	return max_sharpe_port