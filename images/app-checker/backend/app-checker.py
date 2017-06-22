#!/usr/bin/env python

import datetime
import json
import logging
import os
import time

import redis
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

import app
import clonegit

logger = logging.getLogger("app-analyser")
flask_app = Flask(__name__)
CORS(flask_app)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/clear')
def clear():
    r = store()
    r.flushall()

    return "Redis store cleared!"


@flask_app.route('/get')
def get_all():
    r = store()

    apps = []
    for a in list(r.smembers('list')):
        apps.append({
            'name': a,
            'files': json.loads(r.hget('apps:' + a, 'files')),
            'warnings': json.loads(r.hget('apps:' + a, 'warnings')),
            'errors': json.loads(r.hget('apps:' + a, 'errors'))
        })

    return json.dumps({
        'apps': apps,
        'last_scanned': r.get('last_scanned'),
        'total_apps': r.get('total_apps'),
        'flawless': r.get('flawless'),
        'flawed': r.get('flawed'),
        'warnings': r.get('warnings'),
        'errors': json.loads(r.get('errors')),
        'new_installers': r.get('new_installers'),
        'old_installers': r.get('old_installers'),
        'missing_installers': r.get('missing_installers')
    })


@flask_app.route('/get/<app>')
def get_one(app):
    r = store()

    return json.dumps({
        'name': app,
        'files': json.loads(r.hget('apps:' + app, 'files')),
        'warnings': json.loads(r.hget('apps:' + app, 'warnings')),
        'errors': json.loads(r.hget('apps:' + app, 'errors'))
    })


@flask_app.route('/scan')
def scan():
    clonegit.CloneGit()
    get_repositories()

    r = store()
    repodir = os.path.dirname(os.path.realpath(__file__)) + '/repositories'
    subdirs = [x for x in next(os.walk(repodir))[1]]

    apps = []
    flawless = 0
    warnings = 0
    errors = 0
    old_installer = 0
    no_installer = 0

    for name in subdirs:
        if name != 'application-store':
            curr_app = app.App(name, repodir + '/' + name)
            apps.append(curr_app)
            warnings += len(curr_app.warnings)
            errors += len(curr_app.errors)

            if len(curr_app.warnings) == 0 and len(curr_app.errors) == 0:
                flawless += 1

            if curr_app.installer_version(repodir + '/' + name) == 'old':
                old_installer += 1
            elif curr_app.installer_version(repodir + '/' + name) == 'none':
                no_installer += 1

            r.sadd('list', name)
            r.hmset('apps:' + name, {
                'files': json.dumps(curr_app.files),
                'warnings': json.dumps(curr_app.warnings),
                'errors': json.dumps(curr_app.errors)
            })

    pipe = r.pipeline()
    pipe.set('last_scanned', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    pipe.set('total_apps', len(apps))
    pipe.set('flawless', flawless)
    pipe.set('flawed', len(apps) - flawless)
    pipe.set('warnings', warnings)
    pipe.set('errors', errors)
    pipe.set('new_installers', len(apps) - old_installer - no_installer)
    pipe.set('old_installers', old_installer)
    pipe.set('missing_installers', no_installer)
    pipe.execute()

    log_results(apps, flawless, warnings, errors, old_installer, no_installer)

    return json.dumps(list(r.smembers('list')))


def get_repositories():
    directory = os.path.dirname(os.path.realpath(__file__))
    applications = directory + '/repositories/application-store/applications.json'
    with open(applications) as data_file:
        data = json.load(data_file)
    for repositories in data:
        logger.info('Pulling ' + repositories['github_name'])
        clonegit.CloneGit("https://github.com/bibbox/" + repositories['github_name'], repositories['github_name'])


def store():
    redis_db = redis.StrictRedis(host='0.0.0.0', port=6388, db=0, password="bibbox4ever")

    return redis_db


def log_results(apps, flawless, warnings, errors, old_installer, no_installer):
    logger.info('-> Show results\n')
    logger.info('   Total apps          : ' + repr(len(apps)))
    logger.info('   Flawless apps       : ' + repr(flawless) + ' (' + repr(round(float(flawless) / float(len(apps)) * 100.0, 2)) + '%)')
    logger.info('   Flawed apps         : ' + repr(len(apps) - flawless) + ' (' + repr(round(float(len(apps) - flawless) / float(len(apps)) * 100.0, 2)) + '%)\n')
    logger.info('   Total warnings      : ' + repr(warnings))
    logger.info('   Total errors        : ' + repr(errors) + '\n')
    logger.info('   New installers      : ' + repr(len(apps) - old_installer - no_installer) + ' (' + repr(round(float(len(apps) - old_installer - no_installer) / float(len(apps)) * 100.0, 2)) + '%)')
    logger.info('   Old installers      : ' + repr(old_installer) + ' (' + repr(round(float(old_installer) / float(len(apps)) * 100.0, 2)) + '%)')
    logger.info('   Missing installers  : ' + repr(no_installer) + ' (' + repr(round(float(no_installer) / float(len(apps)) * 100.0, 2)) + '%)')


def setup_log():
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('log/app-checker.log')
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


if __name__ == '__main__':
    setup_log()
    logger.handlers[0].flush()

    flask_app.run(debug=True, host='0.0.0.0')
