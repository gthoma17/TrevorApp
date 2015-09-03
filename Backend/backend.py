import web, ConfigParser, json
from os import path
from identitytoolkit import gitkitclient

#read the config file
config = ConfigParser.ConfigParser()
config.read("backend.cfg")

gitkit_config_json = path.join(path.dirname(path.realpath(__file__)), config.get("Google", "GitkitJSON"))
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(gitkit_config_json)



urls = (
	"/", "index",
	"/user/(.*)", "user",
	)
render = web.template.render('templates/')
app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "host"), port=int(config.get("Database", "port")), user=config.get("Database", "user"), pw=config.get("Database", "password"), db=config.get("Database", "name"))

class index:
	def GET(self): 
		return "Shhhh... the database is sleeping."
class user:
	def GET(self, user):
		try:
			theUser = db.query("SELECT * FROM jobAppUsers WHERE email=\'" + user + "\'")[0]
			web.header('Content-Type', 'application/json')
			return json.dumps(theUser)
		except IndexError:
			return None


if __name__ == "__main__":
	app.run()