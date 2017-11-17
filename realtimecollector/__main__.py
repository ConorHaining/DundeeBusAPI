import MySQLdb


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

	# Scrape each bus stop
	scraper.hello();
	pass

if __name__ == '__main__':
	main()