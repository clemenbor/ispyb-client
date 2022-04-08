import sys
import configparser
import requests
import myLogger
import json


def authenticate(url, user, password, site, proxies):
    r = requests.post(url + '/authenticate?site=' + site, headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data={'login': user, 'password': password})
   
    token = (json.loads(r.text)['token'])
   
    return token


def ingest(token, proposers, sessions, samples, labcontacts ):
    proposer = []
    labcontacts = []
    samples = []
    payload = {
        'proposers': proposers,
        'samples': samples,
        'sessions': sessions,
        'labcontacts': labcontacts
    }
  
    r = requests.post(url + '/' + token + '/userportal/ingest', headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data=payload)
    print(r.text)


def readJSONfiles():
    sessions = open("json/sessions.json", "rb").read().decode("latin-1")
    samples = open("json/samples.json", "rb").read().decode("latin-1")
    labcontacts = open("json/labcontacts.json", "rb").read().decode("latin-1")
    proposers = open("json/proposers.json", "rb").read().decode("latin-1")

    return sessions, samples, labcontacts, proposers


if __name__ == "__main__":

    config = configparser.ConfigParser()
    credentialsConfig = configparser.ConfigParser()

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

    token = authenticate(url, user, password, site, proxies)
    if token is None:
        print("Token can not be None")
        sys.exit()

    # reading files from json folder
    sessions, samples, labcontacts, proposers = readJSONfiles()
    ingest(token, proposers, sessions, samples, labcontacts)
