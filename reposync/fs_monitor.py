from __future__ import absolute_import
from multiprocessing import Lock

import logging
from subprocess import Popen, PIPE, call
import re

import pyinotify

log = logging.getLogger()

patterns = [ re.compile(".*/\..*") ]

class GitMonitor(pyinotify.ProcessEvent):
  def my_init(self, branch, monitor, mutex):
    self.monitor = monitor
    self.branch = branch
    self.mutex = mutex

  def process_IN_CLOSE_WRITE(self, event):
    for pattern in patterns:
      if pattern.search(event.pathname) is not None:
        return
    ugly_regex = '%s/\d{4}$' % event.path
    if re.search(ugly_regex, event.pathname) is not None:
      return
    self.mutex.acquire()
    git_status = Popen(['git', 'status', '--porcelain'], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_status_result = git_status.communicate()
    if git_status.returncode != 0:
      log.warn("Error retrieving status {0}\n{1}".format(git_status_result[1], git_status_result[0]))
    if len(git_status_result[0].strip()) == 0:
      log.debug("File change result of git pull: {0}".format(event.pathname))
      self.mutex.release()
      return
    log.debug("adding and committing: {0}".format(event.pathname))
    git_add = Popen(['git', 'add', event.pathname], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_add_result = git_add.communicate()
    if git_add.returncode != 0:
      log.warn("Error adding file: {0} \n {1} \n {2}".format(event.pathname, git_add_result[1], git_add_result[0]))

    git_commit = Popen(['git', 'commit', '-m', 'Added by GitMonitor'], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_commit_result = git_commit.communicate()
    if git_commit.returncode != 0:
      log.warn("Error committing file: {0} \n {1} \n {2}".format(event.pathname, git_commit_result[1], git_commit_result[0]))

    git_push = Popen(['git', 'push', 'origin', self.branch], cwd=event.path, stdout=PIPE, stderr=PIPE)
    git_push_result = git_push.communicate()
    if git_push.returncode != 0:
      log.warn("Error pushing file: {0}\n{1}\n{2}".format(event.pathname, git_push_result[1], git_commit_result[0]))
    self.mutex.release()

class FileSystemMonitor(object):

  def __init__(self, mutex, branch, *dirs):
    self.mutex = mutex
    self.dirs = dirs
    self.branch = branch
    self.wm = pyinotify.WatchManager()
    self.git_monitor = GitMonitor(branch=self.branch, monitor=self.wm, mutex=self.mutex)
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
  monitor = FileSystemMonitor(None,'/tmp/foo')
  monitor.start()
