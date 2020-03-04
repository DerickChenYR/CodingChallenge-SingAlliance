# Mean-Variance Optimization with HuobiAPI
by Derick Chen Yuran

## Documentation

### Project Description

This project seeks to compute the mean-variance optimisation for a portfolio of cryptocurrencies with historical data from HuobiAPI. This was developed for a coding challenge from SingAlliance. 

## Getting Started
* Install dependencies listed under requirements.txt with ```pip```.
* Modify input.txt for your set of inputs, refer to sample_input.txt for format.
* config.json is not included in the Github repository due to security purposes. You should register for an account with Huobi and format the config file as follows:
	```
	{
		"API_keys":{
			"Huobi":{
				"access":"YOUR-ACCESS-KEY",
				"secret":"YOUR-SECRET-KEY",
				"permission":"YOUR-KEY-PERMISSIONS",
				"note":"YOUR-KEY-NOTES",
				"url":"https://api.hbdm.com"
			}
		}
	}
	```
* In commandline, run ```python init.py``` to initiate the script.


### Input Instructions
The input is to be entered via a text file, input.txt
This file should contain 5 lines of inputs

* Line 1: start date for the analysis period, format ```YYYY-MM-DDTHH:MM:SS+HH:MM```
* Line 2: end date for the analysis period, format ```YYYY-MM-DDTHH:MM:SS+HH:MM```
* Line 3: period for the data to be retrieveed. This project currently only supports "60min"
* Line 4: a comma separated list of crypto contracts 
* Line 5: data type to be used in the API. This project currently only supports "quarter"

### Output Instructions
Output of this project can be found under ./outputs/
A PNG graph showing the returns and a text file containing a dictionary of optimal weightages for the portfolio based on maximum Sharpe Ratio will be generated.
Existing files sharing the same names as the default output filenames will be overwritten. 

### Data Source 
The API connects to [https://api.hbdm.com](https://api.hbdm.com)
 to retrieve Huobi Derivatives Market historical data from the Huobi RESTful API.


## Built With
* pandas
* numpy
* matplotlib
* requests


## Author(s)
Derick Chen Yuran - [LinkedIn](https://www.linkedin.com/in/derick-chen/)


## Other Notes
Refer to LICENSE.md for distribution rights of this project.
