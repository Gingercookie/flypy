from datetime import date
import sqlite3
import sys
from config import DATABASE_URL, API_URL, FIELDS, SOLUTION_NUMBER

def create_json_request(options):
	'''Validates inputted options and creates json body for api request'''

	# Validate passenger count
	adults = options['adults']
	children = options['children']
	seniors = options['seniors']
	if not valid_passenger_count(adults, children, seniors):
		print('There must be at least one passenger to book a flight', file=sys.stderr)
		exit(1)

	# Validate To airport code and From airport code
	origin_code = options['origin']
	destination_code = options['destination']
	if not valid_airport_codes(origin_code, destination_code):
		print('Invalid airport code given for origin or destination, check input', file=sys.stderr)
		sys.exit(1)

	# Process the inputted date into api format
	d_str = options['day']	
	api_date = process_date(d_str)

	# Create the response from validated data
	json_request = {
		'request': {
			'passengers':
				{
					'kind': 'qpxexpress#passengerCounts',
					'adultCount': adults,
					'childCount': children,
					'seniors': seniors
				},
			'slice': [
				{
					'kind': 'qpxexpress#sliceInput',
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
	# Create comma separated list of fields from config
	fields = ','.join(FIELDS.values())

	# Create the url from api key and fields
	url = API_URL.format(api_key=api_key, fields=fields)
	
	return url

def valid_passenger_count(*passenger_counts):
	'''Check that there is at least one person on the flight'''
	if sum(passenger_counts) < 1:
		return False

	return True

def valid_airport_codes(*codes):
	'''Checks that all airport codes are valid airports'''
	# Connect to the airport codes database
	connection = sqlite3.connect(DATABASE_URL)
	cursor = connection.cursor()

	# Query the database for the to and from airport code
	for code in codes:
		cursor.execute('SELECT 1 FROM openflights WHERE faacode = ?', (code,))
		
		# Check if the query return True
		row = cursor.fetchone()
		if not row:
			return False

	return True

def process_date(d_str):
	'''Processes the inputted date into API format'''
	try:
		# Check inputted date format
		month, day, year = d_str.split('/')

		# Create a date object to check if month, day, year are valid
		dt_date = date(int(year), int(month), int(day))
	except ValueError:
		print('Invalid date {invalid_date}, check input'.format(invalid_date=d_str), file=sys.stderr)
		sys.exit(1)

	# Process into API form
	api_date = dt_date.strftime('%Y-%m-%d')

	return api_date