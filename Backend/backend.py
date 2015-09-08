import web, ConfigParser, json, string, random
from os import path
from identitytoolkit import gitkitclient

#read the config file
config = ConfigParser.ConfigParser()
config.read("backend.cfg")

urls = (
	"/", "index",
	"/user/(.*)", "user",
	)

app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "host"), port=int(config.get("Database", "port")), user=config.get("Database", "user"), pw=config.get("Database", "password"), db=config.get("Database", "name"))

class index:
	def GET(self): 
		return "Shhhh... the database is sleeping."
class user:
	def GET(self, user):
		try:
			theUser = db.where('jobAppUsers', email=user)[0]
			web.header('Content-Type', 'application/json')
			return json.dumps(theUser)
		except IndexError:
			return "404 Not Found"
	def POST(self, user):
		passedData = dict(web.input())
		reqUser = db.where('jobAppUsers', apiKey=passedData['apiKey'])[0]
		if reqUser['isAdmin']:
			#user is allowed to do this. 
			#first check if user exists.
			newUser = db.where('jobAppUsers', email=user)
			if len(newUser) != 0: #user exists
				return "202 User Updated"
			else: 
				print "passedData['isAdmin'] = " + str(passedData['isAdmin']) + "\n type: " + str(type(passedData['isAdmin']))
				if passedData['isAdmin'] == u'True':
					passedData['isAdmin'] = 1
				else:
					passedData['isAdmin'] = 0
				print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				print passedData['isAdmin']
				print type(passedData['isAdmin'])
				db.insert('jobAppUsers', 
					name=passedData['name'], 
					email=passedData['email'], 
					title=passedData['title'], 
					isAdmin=passedData['isAdmin'], 
					isInTable=1,
					apiKey=makeNewApiKey()
				)
				return "201 User Created"
		else:
			return "403 Forbidden"
def makeNewApiKey():
	potentialApiKey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))
	if len(db.where('jobAppUsers', apiKey=potentialApiKey)) == 0:
		return potentialApiKey
	else:
		return makeNewApiKey()
if __name__ == "__main__":
	app.run()