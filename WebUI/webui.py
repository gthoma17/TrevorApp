import web, ConfigParser, json, sys, urllib
from os import path
from identitytoolkit import gitkitclient

#read the config file
config = ConfigParser.ConfigParser()
config.read("webui.cfg")

gitkit_config_json = path.join(path.dirname(path.realpath(__file__)), config.get("Google", "GitkitJSON"))
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(gitkit_config_json)

urls = (
	"/", "index",
	"/login", "login",
	"/logout", "logout"
	)
render = web.template.render('templates/')
app = web.application(urls, globals())
apiUrl = config.get("Backend", "url")
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': None})
debug = False

class index:
	def GET(self): 
		print "begin"
		gtoken = web.cookies().get('gtoken')
		if gtoken is not None:
			gVars = vars(gitkit_instance.VerifyGitkitToken(gtoken))
			try:
				session.user
			except AttributeError:
				try:
					if session.user['state'] == "unregistered":
						pass
					else:
						session.user = makeUserSession(gVars)
				except AttributeError:
					session.user = makeUserSession(gVars)
			text = "Session Info: " + str(session.user)
		else:
			session.user = {'state':None}
			text = "You are not signed in. Session Info: " + str(session.user)



		if session.user['state'] == "registered":
			text = "You are a registered user "
			if session.user['isAdmin']:
				text += "and an admin.. People like you "
			if debug:
				text += "..... here is your session info: " + str(session.user)
			title = "Welcome back, " + session.user['name'] + "!" 
		elif session.user['state'] == "unregistered":
			text = "You have logged in with Google, but are not a member of this company. Please contact your administrator if you feel you need access" 
			if debug:
				text += ".... here is your session info: " + str(session.user)
			title = "Are you sure you work here?"
		elif session.user['state'] == None:
			text = "Please log in!" 
			if debug:
				text += "Here is your session info: "  + str(session.user)
			title = "Welcome, Stranger!"
		else:
			text = "Strange error. Contact an admin." 
			if debug:
				text += "Here is your session info: "  + str(session.user)
			title = "Wait.. what?"
		return render.index(title, text)	



class login:
	def GET(self):
		return render.login()

class logout:
	def GET(self):
		session.user = {'state':None}
		raise web.seeother('/')

def makeUserSession(gVars):
	session = gVars
	session['state'] = "unregistered"
	#try to ask backend for this user's info
	response = urllib.urlopen(apiUrl+"/user/"+gVars['email']).read()
	if response != "None":
		session['state'] = "registered"
		session.update(dict(json.loads(response)))
	return session


#class session:
#	def GET(self):
#		s = web.ctx.session
#		s.start()
#
#		try:
#			s.click += 1
#		except AttributeError:
#			s.click = 1
#
#		print 'click: ', s.click
#		s.save()



if __name__ == "__main__":
	app.run()