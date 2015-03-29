class Leg:
	'''Each leg of a flight represents one single flight from airport to airport.'''

	def __init__(leg):

		self.arrivalTime = leg[0].value('arrivalTime')
		self.departureTime = leg[0].value('departureTime')
		self.destination = leg[0].value('destination')
		self.destinationTerminal = leg[0].value('destinationTerminal')
		self.duration = leg[0].value('duration')
		self.mileage = leg[0].value('mileage')
		self.origin = leg[0].value('origin')
		self.originTerminal = leg[0].value('originTerminal')
