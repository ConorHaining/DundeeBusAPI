import urllib2
from bs4 import BeautifulSoup
import datetime
import dateparser

def scrape(ATCOCode, updateDatabase):

	# Set the URL which is to be scraped
	url = "http://www.dundeetravelinfo.com/ajax_loadsiristopmonitoringrequest.asp?stopid=" + ATCOCode

	# Open the page
	page = urllib2.urlopen(url)

	# Parse using Beautiful Soup
	html = BeautifulSoup(page, 'lxml')

	isRealtime = realtimeCheck(html)

	if (isRealtime != True):

		return False

		pass

	departureBoard = parseDepartures(html)

	updateDatabase(departureBoard, ATCOCode)

def realtimeCheck(html):

	warning = html.find_all('div', class_='warning')

	if ( len(warning) == 1 ):

		return False

	else:

		return True

	pass

def parseDepartures(html):

	#Find the routes, destination & departure time
	routes = html.find_all('div', class_='route')
	destinations = html.find_all('div', class_='destination')
	departs = html.find_all('div', class_='depart')

	# Next pop of the first element of each of the above
	# This removes the text headers
	routes.pop(0)
	destinations.pop(0)
	departs.pop(0)

	# Create an array to hold the departures
	stopDepartures = []

	for route, destination, depart in zip(routes, destinations, departs):

		departure = {
			'route': route.string,
			'destination': destination.string,
			'departure time': parseDepartureTime(depart.string)
		}

		stopDepartures.append(departure)

		pass

	return stopDepartures

	pass

def parseDepartureTime(time):

	if "NOW" in time:
		departsAt = datetime.datetime.now()
	else:
		departsAt = dateparser.parse('in ' + time)

	return departsAt.strftime("%H:%M")