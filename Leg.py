import logging
from datetime import datetime

class Leg:
	'''Each leg of a flight represents one single flight from airport to airport.'''

	def __init__(self, leg):

		leg_info = leg['leg'][0]

		self.arrivalTime = leg_info['arrivalTime']
		self.departureTime = leg_info['departureTime']
		self.destination = leg_info['destination']
		self.duration = leg_info['duration']
		self.mileage = leg_info['mileage']
		self.origin = leg_info['origin']

	def __str__(self):
		result = ''

		# Removed ':' to make formatting possible
		formattedDepartureDate = self.departureTime.replace(':','')
		pDepartureDateTime = datetime.strptime(formattedDepartureDate, '%Y-%m-%dT%H%M%z')
		pDepartureTime = pDepartureDateTime.strftime('%I:%M %p %Z')
		pDepartureDate = pDepartureDateTime.strftime('%x')

		# Removed ':' to make formatting possible
		formattedArrivalDate = self.arrivalTime.replace(':','')
		pArrivalDateTime = datetime.strptime(formattedArrivalDate, '%Y-%m-%dT%H%M%z')
		pArrivalTime = pArrivalDateTime.strftime('%I:%M %p %Z')
		pArrivalDate = pArrivalDateTime.strftime('%x')

		result += "{} -> {}".format(self.origin, self.destination)
		result += "\n\t\t\tDeparting: {}".format(pDepartureTime)
		result += "\n\t\t\tArriving:  {}".format(pArrivalTime)
		result += "\n\t\t\tDuration:  {} minutes".format(self.duration)

		return result
