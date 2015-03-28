import argparse
from datetime import datetime
import json
import os
import requests
import sys
from pprint import pprint
from config import API_KEY_ENV_VAR, API_URL, USER_AGENT, FIELDS, DEFAULT_SOLUTIONS

def read_api_key():
	api_key = os.environ.get(API_KEY_ENV_VAR)
	if not api_key:
		print('Please set the api key as the environment variable '.format(API_KEY_ENV_VAR))
		sys.exit(1)
	return api_key

def command_line():
	parser = argparse.ArgumentParser(prog='flypy')
	parser.add_argument('-f', '--from', required=True, help='The IATA code of the airport to start from')
	parser.add_argument('-t', '--to', required=True, help='The IATA code of the airport to end at')
	parser.add_argument('-d', '--departure', required=True, help='The date of departure')
	parser.add_argument('--adults', default=1, help='Number of adults to book')
	parser.add_argument('--children', default=0, help='Number of children to book')
	parser.add_argument('--seniors', default=0, help='Number of senior citizens to book')

	args = parser.parse_args()

	return vars(args)

def create_json_request(options):
	request = {
		'request': {
			'passengers':
				{
					'kind': 'qpxexpress#passengerCounts',
					'adultCount': options.get('adults', 0),
					'childCount': options.get('children', 0),
					'seniors': options.get('seniors', 0)
				},
			'slice': [
				{
					'kind': 'qpxexpress#sliceInput',
					'origin': options['from'],
					'destination': options['to'],
					'date': options['departure']
				}
			],
			'solutions': DEFAULT_SOLUTIONS
		}
	}

	return request

def populate_fields():
	fields = ','.join(FIELDS.values())
	return fields

def create_URL(api_key):
	url = API_URL.format(api_key=api_key, fields=populate_fields())
	return url

if __name__ == '__main__':
	# Read the api key
	api_key = read_api_key()

	# Parse the command line options
	args = command_line()

	# Create the json api request
	json_request = create_json_request(args)

	# Set gzip encoding headers
	headers = {'Accept-Encoding:': 'gzip', 'User-Agent:': USER_AGENT}

	# create URL using only requested/desired fields
	url = create_URL(api_key)
	
	# Request the data from the server
	response = requests.post(url, json=json_request, headers=headers)

	# Retrieve the json response
	if response.status_code == requests.codes.ok:
		json_response = response.json()
	else:
		response.raise_for_status()

	# Print out the response
	pprint(json_response)
