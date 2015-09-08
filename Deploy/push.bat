:: Create our working directory
plink -i "C:\Program Files (x86)\PuTTY\work.ppk" greg@gat.im mkdir TrevorApp

:: Delete our local sessions folder
del ../WebUI/sessions

:: SCP up the webui, backend, and deploy script
pscp -r -i "C:\Program Files (x86)\PuTTY\work.ppk" ../webui greg@gat.im:TrevorApp
pscp -r -i "C:\Program Files (x86)\PuTTY\work.ppk" ../backend greg@gat.im:TrevorApp
pscp -i "C:\Program Files (x86)\PuTTY\work.ppk" deploy.sh greg@gat.im:TrevorApp

:: Run the deploy script with plink
plink -i "C:\Program Files (x86)\PuTTY\work.ppk" greg@gat.im sh TrevorApp/deploy.sh