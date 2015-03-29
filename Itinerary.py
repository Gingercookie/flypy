from Leg import Leg

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
		print('Total price: ${}'.format(self.price))
		print('Total flight duration: {}'.format(self.duration))

		for i, leg in enumerate(self.legs):
			print('\n--------------------------------------------------')
			print('Leg #{}'.format(i))
			print(leg)


	def print_top_10(self):
		print('==================================================')
		print('Here are the top 10 results for your search.')
		print('==================================================')
		for i in range(10):
			print('\nFlight Option Number: %d, from %s to %s', i, flights[i].origin, flights[i].destination)

			print('\n--------------------------------------------------')