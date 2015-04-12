import logging
from Leg import Leg
from datetime import datetime

class Itinerary:
	'''Itinerary class is an object that contains exactly one full flight for a trip.'''
	'''Each flight includes all legs of that flight.'''

	# because each flight may be comprised of multiple legs, the dates and places
	# reflect the end goal of the flight, ignoring layovers that may occur.
	def __init__(self, flight):
		self.legs = []
		for leg in flight['slice'][0]['segment']:
			self.legs.append(Leg(leg))

		# grab departure time and date strings from legs
		self.departure = self.legs[0].departure
		self.departure_time_str = self.legs[0].departure_time_str
		self.departure_date_str = self.legs[0].departure_date_str

		# grab arrival time and date strings from legs
		self.arrival = self.legs[-1].arrival
		self.arrival_time_str = self.legs[-1].arrival_time_str
		self.arrival_date_str = self.legs[-1].arrival_date_str

		# grabbing itinerary attributes from legs and json_response
		self.price = float(flight['pricing'][0]['saleTotal'][3:])
		self.duration = sum((leg.duration for leg in self.legs))

	def __str__(self):
		# Header information
		result = "${price}\t{departure_time}\t->\t{arrival_time}\n" \
		"\t\t\t     {departure_date}\t\t\t     {arrival_date}\n" \
		"\tLegs: {num_legs}".format(price=self.price, departure_time=self.departure_time_str, \
		 arrival_time=self.arrival_time_str, departure_date=self.departure_date_str, \
		 arrival_date=self.arrival_date_str, num_legs=len(self.legs))

		# Leg information
		for i, leg in enumerate(self.legs, start=1):
			result += "\n\t\tLeg {}: {}".format(i, leg.__str__())
		result += "\n"
		return result
