import tableprint

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
		headers = ['Origin', 'Departure Time', 'Destination', 'Arrival Time']
		data = [(self.origin, self.departureTime, self.destination, self.arrivalTime)]

		print(self.origin)
		print(self.departureTime)
		print(self.destination)
		print(self.arrivalTime)
		print(data)
		print(headers)

		tableprint.table(data, headers, {'column_width': 20})
		return 'Origin {}'.format(self.origin)
		# print('Departure Time: {}'.format(self.departureTime))
		# print('Destination {}'.format(self.destination))
		# print('Arrival Time: {}'.format(self.arrivalTime))
