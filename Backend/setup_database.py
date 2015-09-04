import MySQLdb, string, random, csv, sys, ConfigParser




def main():
	config = ConfigParser.ConfigParser()
	config.read("backend.cfg")


	#db access info
	HOST = config.get("Database", "host")
	USER = config.get("Database", "user")
	PASSWD = config.get("Database", "password")
	DATABASE = config.get("Database", "name")
	
	# make a connection to the database
	db_connection = MySQLdb.connect(
	        host=HOST,
	        user=USER, 
	        passwd=PASSWD, 
	        )
	
	#create cursor
	cursor = db_connection.cursor()

	#create our database if it doesn't exist
	try:
		cursor.execute('use '+DATABASE)
	except Exception, e:
		createDatabase(DATABASE, cursor)
	finally:
		cursor.execute('use '+DATABASE)

	#create OpenJobs table if it doesn't exist
	if not tblExists("OpenJobs", cursor):
		createOpenJobsTbl(cursor)
	#create ClosedJobs table if it doesn't exist
	if not tblExists("ClosedJobs", cursor):
		createClosedJobsTbl(cursor)

	#create users table if it doesn't exist
	if not tblExists("jobAppUsers", cursor):
		createUsersTbl(cursor)
	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def createDatabase(DATABASE, cursor): 
	#create our database
	print "Creating database: " +DATABASE
	cursor.execute('create database '+DATABASE)

def createOpenJobsTbl(cursor):
	print "Creating table: OpenJobs"
	cursor.execute("""
	CREATE TABLE OpenJobs(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  name VARCHAR(255)  NOT NULL,
	  address TEXT(65535),
	  POC_phone TEXT(65535),
	  POC_email TEXT(65535),
	  description TEXT(65535),
	  PRIMARY KEY(id)
	)
	""")
def createClosedJobsTbl(cursor):
	print "Creating table: ClosedJobs"
	cursor.execute("""
	CREATE TABLE ClosedJobs(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  name VARCHAR(255)  NOT NULL,
	  address TEXT(65535),
	  POC_phone TEXT(65535),
	  POC_email TEXT(65535),
	  description TEXT(65535),
	  PRIMARY KEY(id)
	)
	""")
def createUsersTbl(cursor):
	print "Creating table: jobAppUsers"
	cursor.execute("""
	CREATE TABLE jobAppUsers(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  name VARCHAR(255),
	  title TEXT(65535),
	  email TEXT(65535) NOT NULL,
	  isInTable BOOLEAN,
	  isAdmin BOOLEAN,
	  apiKey TEXT(256),
	  PRIMARY KEY(id)
	)
	""")
	#add Greg's account. Becasue without atlease 1 admin we can't add anyone else.
	apiKey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))
	addGreg = """
	INSERT INTO jobAppUsers
		(id, name, title, email, isInTable, isAdmin, apiKey)
    VALUES
    	(NULL, 'Greg', 'SWE', 'gatlp9@gmail.com', 1, 1, {0})
	"""
	cursor.execute(addGreg.format(sanitize(apiKey)))

def tblExists(name, cursor):
	search_tbl = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = {0}"
	search_tbl = search_tbl.format(sanitize(name))
	cursor.execute(search_tbl)
	if cursor.fetchone()[0] == 1:
		return True
	else:
		return False

def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == "__main__":
	main()	