class Itinerary:
	'''Object to modularize each itinerary separate from another.'''
	'''Each itinerary is being defined as either a one-way, round-trip, or multiple segment trip.'''
	'''Also includes a display method to print to the user in table format.'''

	# dictionary trip_type to detemine if the trip is one-way, round-trip or multiple segment 
	trip_type = {
		0: 'one-way',
		1: 'round-trip',
		2: 'multiple segment',
	}
	
	def __init__(itinerary):
		flights = []
		for flight in itinerary:
			flights.append(Flight(flight))
