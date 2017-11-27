import schedule
import mysql.connector.pooling
import scraper
import config

import Container

def main():

	# Create the container
	container = Container.Container()

	# Establish Database Connection & add it to the container
	cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "bus",
                                                      	  pool_size = 32,
                                                      	  **config.DATABASE_CONFIG)
	container.add('pool', cnxpool)

	# scrape = scraper.Scraper(container, "6400PT1018")
	# scrape.threader()
	cnx = container.get('pool').get_connection()
	cursor = cnx.cursor()

	# Query for all Dundee Bus stops

	cursor.execute('SELECT ATCOCode FROM `bus_stops`')

	for ATCOCode in cursor:

		scrape = scraper.Scraper(container, ATCOCode[0])

		# Scrape every bus stop each minute
		# Tag the job with the ATCOCode so that it can be easily terminated.
		schedule.every(1).minutes.do(scrape.threader).tag(ATCOCode[0])

	cnx.close()

	while 1:
		schedule.run_pending()
		pass

	pass

if __name__ == '__main__':
	main()