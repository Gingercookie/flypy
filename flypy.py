import argparse
import json
import os
import requests
import sys
from pprint import pprint
from config import API_KEY_ENV_VAR, API_URL, USER_AGENT, FIELDS

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
	parser.add_argument('-a', '--arrival', required=True, help='The date of arrival')
	parser.add_argument('--adults', default=1, help='Number of adults to book')
	parser.add_argument('--children', default=0, help='Number of children to book')
	parser.add_argument('--seniors', default=0, help='Number of senior citizens to book')

	args = parser.parse_args()

	return args

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

	# Load the api request from file
	with open('apirequest.json', 'r') as file:
		json_request = json.load(file)

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
