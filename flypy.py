import argparse
import json
import os
import requests
import sys
from pprint import pprint
from preprocessing import create_url, create_json_request
from config import API_KEY_ENV_VAR, USER_AGENT
import itinerary

def get_api_key():
	'''Get the api key from user environment variable'''
	# Read api key from API_KEY_ENV_VAR defined in config
	api_key = os.environ.get(API_KEY_ENV_VAR)

	if not api_key:
		print('Please set the api key as the environment variable '.format(API_KEY_ENV_VAR))
		sys.exit(1)

	return api_key

def command_line():
	'''Define the cli and parse args from stdin'''
	# Define the cli and options
	parser = argparse.ArgumentParser(prog='flypy', description='NEED LONG DESCRIPTION')
	parser.add_argument('-o', '--origin', required=True, help='The FAA code of the airport to start from')
	parser.add_argument('-d', '--destination', required=True, help='The FAA code of the airport to end at')
	parser.add_argument('--day', required=True, help='The date of departure, format MM/DD/YYYY')
	parser.add_argument('-a', '--adults', default=0, type=int, help='Number of adults to book')
	parser.add_argument('-c', '--children', default=0, type=int, help='Number of children to book')
	parser.add_argument('-s', '--seniors', default=0, type=int, help='Number of senior citizens to book')

	# Parse stdin
	args = parser.parse_args()

	# Return dict instead of Namespace
	return vars(args)

def populate_itinerary(json_response):
	itineraries = []

	for itinerary in json_response:
		itineraries.append(Itinerary(itinerary))

if __name__ == '__main__':
	# Read the api key
	api_key = get_api_key()

	# Parse the command line options
	args = command_line()

	# Create the json api request
	json_request = create_json_request(args)

	# Set gzip encoding headers
	headers = {'Accept-Encoding:': 'gzip', 'User-Agent:': USER_AGENT}

	# create URL using only requested/desired fields for output
	url = create_url(api_key)
	
	# Request the data from the server
	response = requests.post(url, json=json_request, headers=headers)

	# Retrieve the json response
	if response.status_code == requests.codes.ok:
		json_response = response.json()
	else:
		response.raise_for_status()

	# create/open an output file to write json response to
	outfile = open('output', 'w')

	# Print out the response
	print(json.dumps(json_response))
