import git
import logging
import os

logger = logging.getLogger("app-analyser")

class CloneGit:

    def __init__(self, url="https://github.com/bibbox/application-store", name="application-store"):
        logger.info('Creating Git object for: ' + url)
        dir = os.path.dirname(os.path.realpath(__file__))
        repo_dir = dir + '/test/repo/' + name
        if(os.path.exists(repo_dir)):
            self.repo = git.Repo(repo_dir)
            origin = self.repo.remotes.origin
            origin.pull()
        else:
            self.repo = git.Repo.clone_from(url, repo_dir, branch='master')
            tags = self.repo.tags
            print(tags)

    def getTags(self):
        tags = self.repo.tags
        print(tags)
        return tags