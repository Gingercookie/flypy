from datetime import date, timedelta
import logging
import sqlite3
from config import OPENFLIGHTS_DATABASE_URL, API_URL, FIELDS, SOLUTION_NUMBER

def create_json_request(options):
	'''Validates inputted options and creates json body for api request'''

	# Validate passenger count
	adults = options['adults']
	children = options['children']
	seniors = options['seniors']
	validate_passenger_count(adults, children, seniors)
		

	# Validate To airport code and From airport code
	origin_code = options['origin']
	destination_code = options['destination']
	validate_airport_codes(origin_code, destination_code)

	# Process the inputted date into api format
	d_str = options['day']	
	api_date = process_date(d_str)

	# Create the response from validated data
	logging.debug('Creating json request')
	json_request = {
		'request': {
			'passengers':
				{
					'adultCount': adults,
					'childCount': children,
					'seniors': seniors
				},
			'slice': [
				{
					'origin': origin_code,
					'destination': destination_code,
					'date': api_date
				}
			],
			'solutions': SOLUTION_NUMBER
		}
	}

	return json_request

def create_url(api_key):
	'''Creates api url containing api key and specifies api output fields from config'''
	logging.debug('Creating url from api key and fields %s from config', ', '.join(FIELDS.keys()))
	# Create comma separated list of fields from config
	fields = ','.join(FIELDS.values())

	# Create the url from api key and fields
	url = API_URL.format(api_key=api_key, fields=fields)
	
	return url

def validate_passenger_count(*passenger_counts):
	'''Check that there is at least one person on the flight and there are positive persons'''
	logging.debug('Validating passenger count')
	# Check if there are negative passengers
	is_negative = lambda i: i < 0
	if any(map(is_negative, passenger_counts)):
		raise ValueError('There cannot be negative passengers for any passenger type')

	if sum(passenger_counts) < 1:
		raise ValueError('There must be at least one passenger to book a flight')

	return True

def validate_airport_codes(*codes):
	'''Checks that all airport codes are valid airports'''
	logging.debug('Validating origin and destination codes')
	
	# Connect to the airport codes database
	logging.debug('Connecting to openflights database at %s', OPENFLIGHTS_DATABASE_URL)
	connection = sqlite3.connect(OPENFLIGHTS_DATABASE_URL)
	cursor = connection.cursor()

	# Query the openflights table for valid FAA codes
	for code in codes:
		logging.debug('Validating FAA code %s', code)
		cursor.execute('SELECT 1 FROM airports WHERE faacode = ?', (code,))
		
		# Check if the query return True
		row = cursor.fetchone()
		if not row:
			raise ValueError('Could not find matching airport for airport code {}'.format(code))

	return True

def process_date(d_str):
	'''Processes the inputted date into API format'''
	logging.debug('Processing inputted date to api format')
	# Check inputted date format
	try:
		month, day, year = map(int, d_str.split('/'))
	except ValueError:
		raise ValueError('Invalid date {invalid_date}, date format should be MM/DD/YYYY'.format(invalid_date=d_str))

	# Attempt to correct YY for YYYY
	if year < 100:
		year += 2000

	# Create a date object to check if month, day, year are valid
	dt_date = date(year, month, day)

	# Check for logical dates to reserve flights
	dt_today = date.today()
	if (dt_today > dt_date):
		raise ValueError('Invalid date {invalid_date}: cannot schedule a flight for a date in the past'.format(invalid_date=d_str))

	if (dt_date - dt_today > timedelta(weeks=52)):
		raise ValueError('Invalid date {invalid_date}: cannot schedule a flight more than one year in the future'.format(invalid_date=d_str))

	# Process into API form
	api_date = dt_date.strftime('%Y-%m-%d')
	logging.debug('Processed input date %s to api date %s', d_str, api_date)

	return api_date