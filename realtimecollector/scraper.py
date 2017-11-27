import urllib2
from bs4 import BeautifulSoup
import datetime
import threading
import config
import mysql.connector
import schedule


class Scraper(object):

	container = None
	ATCOCode = None
	thread = None
	sem = threading.Semaphore(8)
	pool = None

	"""docstring for Scraper"""
	def __init__(self, container, ATCOCode):

		super(Scraper, self).__init__()
		
		self.container = container
		self.ATCOCode = ATCOCode

		self.pool = container.get('pool')

		pass

	def threader(self):

		self.thread = threading.Thread(target=self.scrape, name=self.ATCOCode)
		self.thread.start()

		pass

		
	def scrape(self):

		ATCOCode = self.ATCOCode

		# Set the URL which is to be scraped
		url = "http://www.dundeetravelinfo.com/ajax_loadsiristopmonitoringrequest.asp?stopid=" + ATCOCode

		# Open the page
		self.sem.acquire()
		try:

			page = urllib2.urlopen(url)
			
			pass
		except URLError as e:
			print e
			return

			raise e
		self.sem.release()

		# Parse using Beautiful Soup
		html = BeautifulSoup(page, 'lxml')

		isRealtime = self.realtimeCheck(html)

		departureBoard = self.parseDepartures(html)

		print self.ATCOCode
		self.updateDatabase(departureBoard)

	def realtimeCheck(self, html):
		warning = html.find_all('div', class_='warning')

		if ( len(warning) == 1 ):

			schedule.clear(self.ATCOCode)

			connected = False
			while connected == False:
			
				try:
					cnx = self.pool.get_connection()
					pass
				except mysql.connector.errors.PoolError as e:
					connected = False
					# raise e
				else:
					connected = True
					pass

				pass
			
			cursor = cnx.cursor(prepared=True)
			cursor.execute("UPDATE `bus_stops` SET `realtime`=0 WHERE `ATCOCode`='"+self.ATCOCode+"'")
			cnx.close()
			exit()

		else:

			return True

		pass

	def parseDepartures(self, html):

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
				'departure time': self.parseDepartureTime(depart.string)
			}

			stopDepartures.append(departure)

			pass

		return stopDepartures

		pass

	def parseDepartureTime(self, time):


		if 'Due' in time:

			departsAt = datetime.datetime.now()

		elif "min" in time:

			now = datetime.datetime.now()

			delta = datetime.timedelta(minutes=int(time[:-4]))

			departsAt = now + delta

		else:
			
			today = datetime.date.today()
			now = datetime.datetime.now()

			hour = int(time[:2])
			minute = int(time[3:-1])

			if hour < now.hour:
				today += datetime.timedelta(days=1)
				pass

			time = datetime.time(hour=hour, minute=minute)

			departsAt = datetime.datetime.combine(today, time)

		return departsAt

	def updateDatabase(self, departures):

		connected = False
		while connected == False:
		
			try:
				cnx = self.pool.get_connection()
				pass
			except mysql.connector.errors.PoolError as e:
				connected = False
				# raise e
			else:
				connected = True
				pass

			pass
		
		cursor = cnx.cursor(prepared=True)

		# Clear out stale depatures
		cursor.execute("DELETE FROM dundeebus.departures WHERE `stop`='"+self.ATCOCode+"';")
		cnx.commit()
		#departure['route']+"', '"+departure['destination']+"','"+departure['departure time'].strftime("%Y-%m-%d %H:%M")+"', '"+self.ATCOCode+"')

		query = "INSERT INTO `departures` (`route`, `destination`, `departure`, `stop`) VALUES (%s, %s, %s, %s)"
		for departure in departures:

			cursor.execute(query, (departure['route'], departure['destination'], departure['departure time'].strftime("%Y-%m-%d %H:%M"), self.ATCOCode))
			cnx.commit()
			pass

		cnx.close()

		pass



		pass
