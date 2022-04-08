import sys
import time
import configparser
import requests
import myLogger
import json
from pydesydoor.doorispybjava import DoorISPyBJava


def authenticate(url, user, password, site, proxies):
    r = requests.post(url + '/authenticate?site=' + site, headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data={'login': user, 'password': password})
    token = (json.loads(r.text)['token'])
    return token


def ingest(token, proposers, sessions, samples, labcontacts):
    payload = {
        'proposers': proposers,
        'samples': samples,
        'sessions': sessions,
        'labcontacts': labcontacts
    }
    r = requests.post(url + '/' +token + '/userportal/ingest', headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=proxies, data=payload)


if __name__ == "__main__":

    config = configparser.ConfigParser()
    credentialsConfig = configparser.ConfigParser()

    # Configuration files
    config.read('ispyb.properties')
    credentialsConfig.read('credentials.properties')

    user = str(credentialsConfig.get('Credential', 'user'))
    password = str(credentialsConfig.get('Credential', 'password'))
    site = str(credentialsConfig.get('Credential', 'site'))
    filename = str(credentialsConfig.get('Source', 'file'))

    url = str(config.get('Connection', 'url'))
    proxy_http = str(config.get('Proxy', 'http'))
    proxy_https = str(config.get('Proxy', 'https'))

    myLogger.printConfiguration(user, password, url)
    print("Processing DOOR proposals from file: {}".format(filename))

    proxies = {
      'http': proxy_http,
      'https': proxy_https,
    }

    token = authenticate(url, user, password, site, proxies)
    if token is None:
        print("Token can not be None")
        sys.exit()
    
    # Read the file with DOOR proposal codes to update
    with open(filename) as file:
        lines = file.read().splitlines()

    client = DoorISPyBJava()
    start_time = time.time()
    time.ctime()
    print("Starting the sync process between DOOR and ISPyB at {}"
          .format(time.strftime('%H:%M:%S %Z on %b %d, %Y')))
    for proposal_id in lines:
        print("--- Updating DOOR proposal: %s" % proposal_id)
        start_proposal = time.time()
        proposers = client.get_proposers(proposal_id)
        labcontacts = client.get_labcontacts(proposal_id)
        sessions = client.get_sessions(proposal_id)
        # Samples will not be imported by now
        samples = []
        ingest(token, proposers, sessions, samples, labcontacts)
        print("------ Finished updating DOOR proposal: %s ---took %s seconds ---" %
              (proposal_id, time.time() - start_proposal))
    time.ctime()
    print("DESYUpdater finished at {}"
          .format(time.strftime('%H:%M:%S %Z on %b %d, %Y')))
