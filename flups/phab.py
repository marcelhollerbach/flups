from phabricator import Phabricator
import subprocess

class Phab:
  def __init__(self, config):
    self.config = config
    self.phab = Phabricator(host=config.phabricator_url, token=config.phabricator_token)
    self.phab.connect()
    self.phab.update_interfaces()

  def notify_harbourmaster(self, buildTargetPHID, success):
    self.phab.harbormaster.sendmessage(buildTargetPHID=buildTargetPHID, type=success)

  def apply_patch(self, id):
    if subprocess.call(["git", "-C", self.config.repository_path, "phab", "apply", id]) != 0:
      return False
    return True
