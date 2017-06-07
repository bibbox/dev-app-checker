#!/usr/bin/env python

import logging
import time
import os
import json

import clonegit
import neo4japp

logger = logging.getLogger("app-analyser")

def setupLog():
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('log/app-analyser.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

def getRepositorys():
    dir = os.path.dirname(os.path.realpath(__file__))
    applications = dir + '/test/repo/application-store/applications.json'
    with open(applications) as data_file:
        data = json.load(data_file)
    for repositories in data:
        print(repositories['github_name'])
        clonegit.CloneGit("https://github.com/bibbox/" + repositories['github_name'], repositories['github_name'])

if __name__ == '__main__':
    setupLog()
    logger.info('Start App-Analyser')
    logger.info('------------------')

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')

    clonegit.CloneGit()
    getRepositorys()

    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

    neo4japp.Neo4jApp()

    logging.debug('wat wat')
    logger.handlers[0].flush()