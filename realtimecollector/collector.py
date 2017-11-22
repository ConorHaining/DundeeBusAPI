import schedule
import time
import json
import dateparser
import datetime
import csv
import MySQLdb
import urllib2
from bs4 import BeautifulSoup

def scheduleTimer(due):

	now = datetime.datetime.now()

	


	pass


def scrape(stopID):
	print("I'm working on " + stopID)

	#set the URL which is being scraped
	url = "http://www.dundeetravelinfo.com/ajax_loadsiristopmonitoringrequest.asp?stopid=" + stopID

	#open the URL
	page = urllib2.urlopen(url)

	#parse the webpage
	soup = BeautifulSoup(page, "lxml")

	#print it
	#print soup.prettify()

	# Check if there has been a warning delivered
	warning = soup.find_all('div', class_='warning')
	if( warning != []):
		print "No realtime data for: " + stopID

		# Update DB
		try:
			updates = db.cursor()
			updates.execute("UPDATE `bus_stops` SET `realtime`=0 WHERE `ATCOCode`='" + stopID +"'")
			db.commit()
		except MySQLdb.Error, e:
		    try:
		        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		    except IndexError:
		        print "MySQL Error: %s" % str(e)
		# Cancel Job
		schedule.clear(stopID)

		return;

	#Find the routes, destination & departure time
	routes = soup.find_all('div', class_='route')
	destinations = soup.find_all('div', class_='destination')
	departs = soup.find_all('div', class_='depart')

	# Next pop of the first element of each of the above
	# This removes the text headers
	routes.pop(0)
	destinations.pop(0)
	departs.pop(0)

	stopDepartures = [];

	for route, destination, time in zip(routes, destinations, departs):

		# Perform time parsing
		try:
			time = dateparser.parse('in'  + time.string) # Parse options, prefer future
			pass
		except TypeError as e:
			print "ERROR: Stop ID" + stopID
			return
			raise e
		else:
			pass

		try:
			details = {
				'route': route.string,
				'destination' : destination.string,
				'departure': time.strftime("%H:%M")
			}
			pass
		except AttributeError as e:
			print "LOG: error at " + stopID
			return

		stopDepartures.append(details)

		inserts = db.cursor()
		# inserts.execute('INSERT INTO `departures` (`route`, `destination`, `departure`, `stop`) VALUES (`'+details['route']+'`, `'+details['destination']+'`,`'+details['departure']+'`, `'+stopID+'`)')
		inserts.execute("INSERT INTO `departures` (`route`, `destination`, `departure`, `stop`) VALUES ('"+details['route']+"', '"+details['destination']+"','"+details['departure']+"', '"+stopID+"')")
		db.commit()

		pass

# Connect to the DB and query all stops
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="WestPark6!",  # your password
                     db="dundeebus")        # name of the data base

cur = db.cursor()

cur.execute("SELECT * FROM bus_stops")

for stop in cur.fetchall():
    schedule.every(1).minutes.do(scrape, stop[1]).tag(stop[1])

# scrape("6400L00115")

while True:
    schedule.run_pending()
    # scrape
    time.sleep(1)