from __future__ import absolute_import

import logging
from subprocess import Popen, PIPE, call
import re

import pyinotify

log = logging.getLogger()

pattern = re.compile(".*\..*")

class GitMonitor(pyinotify.ProcessEvent):
  def my_init(self, monitor):
    self.monitor = monitor

  def process_IN_CLOSE_WRITE(self, event):
    if pattern.search(event.pathname) is not None:
      return
    log.info("event: {0}".format(event))
    log.info("adding and committing: {0}".format(event.pathname))
    git_add = Popen(['git', 'add', event.pathname], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_add_result = git_add.communicate()
    if git_add.returncode != 0:
      log.warn("Error adding file: {0} \n {1} \n {2}".format(event.pathname, git_add_result[1], git_add_result[0]))

    git_commit = Popen(['git', 'commit', '-m', 'Added by GitMonitor'], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_commit_result = git_commit.communicate()
    if git_commit.returncode != 0:
      log.warn("Error committing file: {0} \n {1} \n {2}".format(event.pathname, git_commit_result[1], git_commit_result[0]))


class FileSystemMonitor(object):

  def __init__(self, *dirs):
    self.dirs = dirs
    self.wm = pyinotify.WatchManager()
    self.git_monitor = GitMonitor(monitor=self.wm)
    self.notifier = pyinotify.Notifier(self.wm, default_proc_fun=self.git_monitor)
    self.watch_list = []

  def start(self):
    for d in self.dirs:
      log.info("Adding dir: {0}".format(d))
      self.watch_list.append(self.wm.add_watch(d, pyinotify.ALL_EVENTS, rec=True, auto_add=True))
    self.notifier.loop()

if __name__ == '__main__':
  FORMAT = '%(asctime)-15s %(message)s'
  logging.basicConfig(format=FORMAT, level=logging.INFO)
  monitor = FileSystemMonitor('/tmp/foo')
  monitor.start()
