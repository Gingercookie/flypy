import json
import requests
from pprint import pprint
from config import API_KEY

REST_API = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key={}'

if __name__ == '__main__':
	# Load the api request from file
	with open('apirequest.json', 'r') as file:
		json_request = json.load(file)

	# Request the data from the server
	response = requests.post(REST_API.format(API_KEY), json=json_request)
	
	# Retrieve the json response
	if response.status_code == requests.codes.ok:
		json_response = response.json()
	else:
		response.raise_for_status()

	# Print out the response
	pprint(json_response)