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

		self.price = flight['pricing'][0]['saleTotal']
		self.arrivalDate = self.legs[-1].arrivalTime
		self.departureDate = self.legs[0].departureTime
		self.duration = sum((leg.duration for leg in self.legs))

	def __str__(self):
		# create pretty looking (printable) itinerary attributes
		pPrice = self.price.split('.')[0][3:]

		# Removed ':' to make formatting possible
		formattedDepartureDate = self.departureDate.replace(':','')
		pDepartureDateTime = datetime.strptime(formattedDepartureDate, '%Y-%m-%dT%H%M%z')
		pDepartureTime = pDepartureDateTime.strftime('%I:%M %p %Z')
		pDepartureDate = pDepartureDateTime.strftime('%x')

		# Removed ':' to make formatting possible
		formattedArrivalDate = self.arrivalDate.replace(':','')
		pArrivalDateTime = datetime.strptime(formattedArrivalDate, '%Y-%m-%dT%H%M%z')
		pArrivalTime = pArrivalDateTime.strftime('%I:%M %p %Z')
		pArrivalDate = pArrivalDateTime.strftime('%x')

		# create pretty looking lists of formatted leg attributes
		formattedLegDepartures = []
		formattedLegArrivals = []
		origins = []
		destinations = []
		durations = []

		for a, i in enumerate(self.legs):
			# populate the formatted leg departures list
			formattedLegDate = self.legs[a].departureTime.replace(':','')
			pLegDepartureDateTime = datetime.strptime(formattedLegDate, '%Y-%m-%dT%H%M%z')
			formattedLegDepartures.append(pLegDepartureDateTime)

			# populate the formatted leg arrivals list
			formattedLegDate = self.legs[a].arrivalTime.replace(':','')
			pLegArrivalDateTime = datetime.strptime(formattedLegDate, '%Y-%m-%dT%H%M%z')
			formattedLegArrivals.append(pLegArrivalDateTime)

			# populate the list of origins and destinations
			origins.append(self.legs[a].origin)
			destinations.append(self.legs[a].destination)
			durations.append(self.legs[a].duration)


		# Header information
		result = "${}".format(pPrice)
		result += "\t{})".format(pDepartureTime)
		result += "\t->\t{}".format(pArrivalTime)
		result += "\n\t\t\t     {}".format(pDepartureDate)
		result += "\t\t\t     {}".format(pArrivalDate)
		result += "\n"

		# Leg information
		result += "\tLegs: {}".format(len(self.legs))
		for i, leg in enumerate(self.legs, start=1):

			# pull out formatted datetime information for current iteration of legs
			pLegDepartureTime = formattedLegDepartures[i-1].strftime('%I:%M %p %Z')
			pLegDepartureDate = formattedLegDepartures[i-1].strftime('%x')
			pLegArrivalTime = formattedLegArrivals[i-1].strftime('%I:%M %p %Z')
			pLegArrivalDate = formattedLegArrivals[i-1].strftime('%x')

			result += "\n\t\tLeg {}: {} -> {}".format(i, origins[i-1], destinations[i-1])
			result += "\n\t\t\tDeparting: {}".format(pLegDepartureTime)
			result += "\n\t\t\tArriving:  {}".format(pLegArrivalTime)
			result += "\n\t\t\tDuration:  {} minutes".format(durations[i-1])


		result += "\n"

		return result
