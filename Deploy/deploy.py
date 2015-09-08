import os, shutil, sys, ConfigParser
from subprocess import call

config = ConfigParser.ConfigParser()
config.read("deploy.cfg")

plink = config.get("Deploy", "remoteCommandProg")
scp = config.get("Deploy", "scp")
key = config.get("Deploy", "sshKey")
user = config.get("Deploy", "user")
app = config.get("Deploy", "appName")
host = config.get("Deploy", "host")

def main():
	# change working directory to the app's root
	os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
	os.chdir("..")

	#remove session folder
	try:
		shutil.rmtree("WebUI"+os.sep+"sessions")
	except:
		#don't care if it didn't exist.
		pass

	#create our remote working directory
	command = plink+" -i  "+key+" "+user+"@"+host+" mkdir "+app
	call(command)

	#scp up our files
	command = scp+" -r -i  "+key+" webui "+user+"@"+host+":"+app
	call(command)
	command = scp+" -r -i  "+key+" backend "+user+"@"+host+":"+app
	call(command)
	command = scp+" -r -i  "+key+" Deploy"+os.sep+"deploy.sh "+user+"@"+host+":"+app
	call(command)

	#run the deploy script on our server
	command = plink+" -i  "+key+" "+user+"@"+host+" sh "+app+"/deploy.sh"
	call(command)

if __name__ == "__main__":
	main()