import csv
import requests
import sqlite3
from config import OPENFLIGHTS_DATABASE_URL

OPENFLIGHTS_URL = '''https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat?format=raw'''

def get_database_csv():
	'''Retrieve csv from OpenFlights Source Forge page'''
	response = requests.get(OPENFLIGHTS_URL)
	if response.status_code == requests.codes.ok:
		return response.content.decode('UTF8', 'strict'	)
	else:
		response.raise_for_status()

if __name__ == '__main__':
	# Get csv database from OpenFlights Source Forge page
	openflights_csv = get_database_csv()

	# Get a csv reader of the csv
	openflights_csv_reader = csv.reader(openflights_csv.splitlines())

	# Create database and cursor
	connection = sqlite3.connect(OPENFLIGHTS_DATABASE_URL)
	cursor = connection.cursor()

	# Create table for csv values
	cursor.execute('''CREATE TABLE airports(airportid INTEGER, airportname TEXT, cityname TEXT, countryname TEXT, '''
		'''faacode TEXT, icaocode TEXT, latitude REAL, longitude REAL, altitude INTEGER, houroffsetutc REAL, dst TEXT, timezone TEXT)''')
	
	# Input each csv row into the database
	for row in openflights_csv_reader:
		cursor.execute('''INSERT INTO airports VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

	# Commit and close
	connection.commit()
	connection.close()