import logging
from datetime import datetime

class Leg:
	'''Each leg of a flight represents one single flight from airport to airport.'''

	def __init__(self, leg):

		leg_info = leg['leg'][0]

		# Removed ':' to make formatting possible
		# create arrival and departure datetime objects
		formattedArrivalDate = leg_info['arrivalTime'].replace(':','')
		formattedDepartureDate = leg_info['departureTime'].replace(':','')
		self.arrival = datetime.strptime(formattedArrivalDate, '%Y-%m-%dT%H%M%z')
		self.departure = datetime.strptime(formattedDepartureDate, '%Y-%m-%dT%H%M%z')

		# generating strings from arrival/departure datetimes
		self.departure_time_str = self.departure.strftime('%I:%M %p %Z')
		self.departure_date_str = self.departure.strftime('%x')
		self.arrival_time_str = self.arrival.strftime('%I:%M %p %Z')
		self.arrival_date_str = self.arrival.strftime('%x')

		# grabbing leg information from json_response
		self.destination = leg_info['destination']
		self.duration = leg_info['duration']
		self.mileage = leg_info['mileage']
		self.origin = leg_info['origin']

	def __str__(self):
		return "{origin} -> {destination}\n" \
		"\t\t\tDeparting: {departure_time}\n" \
		"\t\t\tArriving:  {arrival_time}\n" \
		"\t\t\tDuration:  {duration} minutes".format(origin=self.origin, \
		destination=self.destination, departure_time=self.departure_time_str, \
		arrival_time=self.arrival_time_str, duration=self.duration)
