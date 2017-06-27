import os
import logging
import json

logger = logging.getLogger("app-analyser")


class App:

    files2check = [
        'icon.png',
        'README.md',
        'INSTALL-APP.md',
        'appinfo.json',
        'sys-info.json',
        'portinfo.json',
        'file_structure.json',
        'id-mapping-info.json',
        'config-parameters.json',
        'environment-parameters.json',
        'docker-compose-template.yml'
    ]

    suggested_files = [
        'icon.png',
        'README.md',
        'INSTALL-APP.md'
    ]

    required_files = [
        'appinfo.json',
        'sys-info.json',
        'portinfo.json',
        'file_structure.json',
        'docker-compose-template.yml'
    ]

    appinfo_params = [
        'name',
        'short_name',
        'version',
        'description',
        'short_description',
        'catalogue_url',
        'application_url',
        'tags',
        'application_documentation_url'
    ]

    file_structure_params = [
        'makefolders',
        'copyfiles'
    ]

    portinfo_params = [
        'mappings'
    ]

    sys_info_params = [
        'runningcontainers',
        'supportcontainers'
    ]

    def __init__(self, name, dir):
        self.warnings = []
        self.errors = []
        self.files = []

        logger.info('----> Scanning repository:' + ' ' * 15 + name)
        self.show_stats(name, dir)

    def show_stats(self, name, dir):
        for file in self.files2check:
            logger.info(' ' * 6 + file + ' ' * (35 - len(file)) + ': ' + self.file_exists(dir + '/' + file))
            self.files.append({
                'name': file,
                'status': self.file_exists(dir + '/' + file)
            })

            if not os.path.isfile(dir + '/' + file):
                if file in self.required_files:
                    self.errors.append('Missing required file ' + file + ' for app ' + name)
                elif file in self.suggested_files:
                    self.warnings.append('Missing suggested file ' + file + ' for app ' + name)

            # Check parameters for some JSON files
            if file == 'appinfo.json':
                self.check_params(dir, 'appinfo.json', name, self.appinfo_params)
            elif file == 'sys-info.json':
                self.check_params(dir, 'sys-info.json', name, self.sys_info_params)
            elif file == 'portinfo.json':
                self.check_params(dir, 'portinfo.json', name, self.portinfo_params)
            elif file == 'file_structure.json':
                self.check_params(dir, 'file_structure.json', name, self.file_structure_params)

        logger.info(' ' * 6 + 'Installer version' + ' ' * 18 + ': ' + self.installer_version(dir) + '\n')

        if self.installer_version(dir) == 'old' or self.installer_version(dir) == 'none':
            self.errors.append('Installer version for app ' + name + ' is ' + self.installer_version(dir))

        logger.info(' ' * 6 + 'Warnings detected' + ' ' * 18 + ': ' + repr(len(self.warnings)))

        if len(self.warnings) > 0:
            for war in self.warnings:
                logger.warning(' ' * 8 + '- ' + war)

        logger.info(' ' * 6 + 'Errors detected' + ' ' * 20 + ': ' + repr(len(self.errors)))

        if len(self.errors) > 0:
            for err in self.errors:
                logger.error(' ' * 8 + '- ' + err)

    def file_exists(self, file):
        if os.path.isfile(file):
            return 'exists'
        else:
            return 'does not exist'

    def installer_version(self, dir):
        if os.path.isfile(dir + '/file_structure.json'):
            return 'new'
        elif os.path.isfile(dir + '/install.sh'):
            return 'old'
        else:
            return 'none'

    def check_params(self, dir, file, app, params):
        if os.path.isfile(file):

            with open(dir + '/' + file) as data_file:
                try:
                    data = json.load(data_file)
                except ValueError, e:
                    logger.warning(' ' * 43 + '--> invalid JSON formatting!')
                    self.warnings.append('Invalid JSON formatting for file ' + file + ' of app ' + app)
                    return False

                for attr in params:
                    if attr not in data:
                        logger.warning(' ' * 43 + '--> missing parameter : ' + attr)
                        self.warnings.append('Missing JSON parameter ' + attr + ' for file ' + file + ' of app "' + app)
                    # elif len(data[attr]) == 0:
                        # print ' ' * 43 + '--> empty parameter   : ' + attr
