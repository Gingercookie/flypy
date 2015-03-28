FIELDS = {
	'arrivalDate': 			'trips/tripOption/slice/segment/leg/arrivalTime',
	'departureDate': 		'trips/tripOption/slice/segment/leg/departureTime',
	'from': 				'trips/tripOption/slice/segment/leg/origin',
	'to':	 				'trips/tripOption/slice/segment/leg/destination',
	'duration':	 			'trips/tripOption/slice/segment/leg/duration',
	'originTerminal':		'trips/tripOption/slice/segment/leg/originTerminal',
	'destinationTerminal':	'trips/tripOption/slice/segment/leg/destinationTerminal',
	'mileage':				'trips/tripOption/slice/segment/leg/mileage',
	'layoverDuration':		'trips/tripOption/slice/segment/leg/connectionDuration',
	'changePlane':			'trips/tripOption/slice/segment/leg/changePlane',
	'baggage':				'trips/tripOption/pricing/segmentPricing/freeBaggageOption/pieces',
	'price': 				'trips/tripOption/pricing/saleTotal',
	'refundable':			'trips/tripOption/pricing/refundable'
}

API_URL = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key={}'
API_KEY_ENV_VAR = 'FLYPY_APIKEY'
USER_AGENT = 'fuzzy-trip-planningv0.1 (gzip)'