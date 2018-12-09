from phabricator import Phabricator

class Phab:
  def __init__(self, config):
    self.config = config
    self.phab = Phabricator(host=config.phabricator_url, token=config.phabricator_token)
    self.phab.connect()
    self.phab.update_interfaces()

  def notify_harbourmaster(self, buildTargetPHID, success):
    args = {}
    args['buildTargetPHID'] = buildTargetPHID
    args['type'] = "Fail"
    self.phab.harbormaster.sendmessage(buildTargetPHID=buildTargetPHID, type="Fail")

  def apply_patch(self, id):
    subprocess.call(["git", "-C", self.config.repository_path, "phab", "apply", id])
    return True
