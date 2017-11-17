import MySQLdb
import schedule

import scraper
import config


def main():

	# Establish Database Connection

	db = MySQLdb.connect(
			host=config.DATABASE_CONFIG['host'],
			user=config.DATABASE_CONFIG['user'],
			passwd=config.DATABASE_CONFIG['passwd'],
			db=config.DATABASE_CONFIG['database']
		)

	# Query for all Dundee Bus stops

	cursor = db.cursor()

	cursor.execute('SELECT * FROM `bus_stops`')

	for stop in cursor.fetchall():

		ATCOCode = stop[1]

		# Scrape every bus stop each minute
		# Tag the job with the ATCOCode so that it can be easily terminated.
		schedule.every(1).minutes.do(scraper.scrape, ATCOCode).tag(ATCOCode)


	while 1:
		schedule.run_pending()
		pass

	pass

if __name__ == '__main__':
	main()