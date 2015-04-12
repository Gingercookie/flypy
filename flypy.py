import argparse
import logging
import os
import requests
import sys

from preprocessing import create_url, create_json_request
from config import API_KEY_ENV_VAR, USER_AGENT, LOG_FORMAT, LOG_DATE_FORMAT
from Itinerary import Itinerary

def get_api_key():
	'''Get the API key from user environment variable'''
	logging.debug('Retriving API key from environment variable %s', API_KEY_ENV_VAR)
	# Read API key from API_KEY_ENV_VAR defined in config
	api_key = os.environ.get(API_KEY_ENV_VAR)

	if not api_key:
		raise OSError('Please set the API key as the environment variable {env_var}'.format(env_var=API_KEY_ENV_VAR))

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
	parser.add_argument('--debug', action='store_true', help='Toggles sending debugging messages to the log')

	args = parser.parse_args()

	# Return dict instead of Namespace
	return vars(args)

def setup_logging(debug):
	'''Set up logging for the system'''
	# Toggle debugging mode if debug flag is set
	level = logging.DEBUG if debug else logging.INFO
	logging.basicConfig(filename='flypy.log', level=level, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

def print_top_itineraries(itineraries):

	print("Top Flights")
	print("-----------")

	for num, itinerary in enumerate(itineraries[:10], start=1):
		print("Itinerary #{:2}:".format(num),
			itinerary)

def main():
	# Parse the command line options
	args = command_line()

	# Set up logging for the program
	setup_logging(args['debug'])

	# Read the api key
	try:
		api_key = get_api_key()
	except OSError as e:
		logging.exception('Could not retrieve API key from %s', API_KEY_ENV_VAR)
		print(e, file=sys.stderr)
		sys.exit(1)

	# Create the json api request
	try:
		json_request = create_json_request(args)
	except ValueError as e:
		logging.exception('Preprocessing Error')
		print(e, file=sys.stderr)
		sys.exit(1)

	# create URL using only requested/desired fields for output
	url = create_url(api_key)

	# Set gzip encoding headers
	headers = {'Accept-Encoding:': 'gzip', 'User-Agent:': USER_AGENT}

	# Request the data from the server
	logging.info('Sending request to API')
	response = requests.post(url, json=json_request, headers=headers)

	# Retrieve the json response
	if response.status_code == requests.codes.ok:
		json_response = response.json()
	else:
		try:
			response.raise_for_status()
		except Exception as e:
			logging.exception('Non-OK status code from Google API')
			raise e

	# create a list of itineraries
	json_trip_options = json_response['trips']['tripOption']
	itineraries = list(map(Itinerary, json_trip_options))
	
	# Print the top itineraries
	print_top_itineraries(itineraries)

if __name__ == '__main__':
	main()
