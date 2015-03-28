import json
import os
import requests
import sys
from pprint import pprint
from config import API_KEY_ENV_VAR, API_URL, USER_AGENT

def read_api_key():
	api_key = os.environ.get(API_KEY_ENV_VAR)
	if not api_key:
		print('Please set the api key as the environment variable '.format(API_KEY_ENV_VAR))
		sys.exit(1)
	return api_key

if __name__ == '__main__':
	# Read the api key
	api_key = read_api_key()

	# Load the api request from file
	with open('apirequest.json', 'r') as file:
		json_request = json.load(file)

	# Set gzip encoding headers
	headers = {'Accept-Encoding:': 'gzip', 'User-Agent:': USER_AGENT}

	# Request the data from the server
	response = requests.post(API_URL.format(api_key), json=json_request, headers=headers)

	# Retrieve the json response
	if response.status_code == requests.codes.ok:
		json_response = response.json()
	else:
		response.raise_for_status()

	# Print out the response
	pprint(json_response)
