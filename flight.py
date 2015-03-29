class Flight:
	'''Flight class is an object that contains exactly one full flight for a trip.'''
	'''Each flight includes all legs of that flight.'''

	# because each flight may be comprised of multiple legs, the dates and places
	# reflect the end goal of the flight, ignoring layovers that may occur.
	def __init__(flight):
		legs = []
		for leg in flight:
			legs.append(Leg(leg[0].value('slice')[0]))

		price = flight[0].value('pricing')[0].value('saleTotal')
		self.arrivalDate = legs[len(legs)-1].arrivalDate
		self.departureDate = legs[0].departureDate
		self.origin = legs[0].origin
		self.destination = legs[len(legs)-1].destination
		
		for x in legs:
			self.duration += legs[x].duration
