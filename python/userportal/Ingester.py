import traceback
import sys
from suds.client import Client
from suds.transport.http import HttpAuthenticated
import os, shutil
from contextlib import closing
from distutils.util import strtobool
from datetime import datetime
from random import randint
import time
import base64
import ConfigParser
from operator import itemgetter
import requests
import myLogger
import json

def user_yes_no_query(question):
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')	

def authenticate(url, user, password, site, proxies):
    r = requests.post(url + '/authenticate?site=' + site, headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data={'login': user, 'password': password})
   
    token = (json.loads(r.text)['token'])
   
    return token
  
def ingest(token, proposers, scientists, sessions, samples, labcontacts ):

    payload = {
		'proposers' 	: proposers, 
		'samples'	: samples, 
		'sessions'	: sessions,
		'labcontacts'	:labcontacts
    }
  
    r = requests.post(url + '/' +token + '/userportal/ingest', headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data=payload)
    print(r.text)


def readJSONfiles():
    scientists = open("json/scientists.json", "r").read()
    sessions = open("json/sessions.json", "r").read()   
    samples = open("json/samples.json", "r").read()   
    labcontacts = open("json/labcontacts.json", "r").read() 
    labcontact = open("json/labcontact.json", "r").read() 
    proposers = open("json/proposers.json", "r").read()      

    return scientists,sessions,samples,labcontacts,labcontact,proposers




if __name__ == "__main__":

	config = ConfigParser.ConfigParser()
	credentialsConfig = ConfigParser.ConfigParser()

	# Configuration files
	config.read('ispyb.properties')	
	credentialsConfig.read('credentials.properties')

	user = str(credentialsConfig.get('Credential', 'user'))
	password = str(credentialsConfig.get('Credential', 'password'))
        site = str(credentialsConfig.get('Credential', 'site'))

	url = str(config.get('Connection', 'url'))
        proxy_http = str(config.get('Proxy', 'http'))
        proxy_https = str(config.get('Proxy', 'https'))

	myLogger.printConfiguration(user, password, url)
	

        proxies = {
	  'http': proxy_http,
	  'https': proxy_https,
	}

	if (user_yes_no_query("Are these values OK?") == False):
		print("Exit")
		sys.exit()
               
        token = authenticate(url, user, password, site, proxies)
        if token is None:
             print("Token can not be None")
             sys.exit()

        # reading scientists.json
        scientists,sessions,samples,labcontacts,labcontact,proposers = readJSONfiles()
        ingest(token, proposers,scientists,sessions,samples,labcontacts)
