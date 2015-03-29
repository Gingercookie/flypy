import flight

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

	def print_top_10():
		print('==================================================')
		print('Here are the top 10 results for your search.')
		print('==================================================')
		for i in range(10):
			print('\nFlight Option Number: %d, from %s to %s', i, flights[i].origin, flights[i].destination)
			print('Total price: $%d USD', flights[i].price)
			print('Departure Time: %s', flights[i].departureDate)
			print('Departure Terminal: %d', flights[i].departureTerminal)
			print('Arrival Time: %s', flights[i].arrivalDate)
			print('Arrival Terminal: %d', flights[i].arrivalTerminal)
			print('Duration: %d', flights[i].duration)
			print('\n--------------------------------------------------')

