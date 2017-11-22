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