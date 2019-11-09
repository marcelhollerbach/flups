from phabricator import Phabricator
import subprocess
import re

class Phab:
  def __init__(self, config):
    self.config = config
    self.phab = Phabricator(host=config.phabricator_url, token=config.phabricator_token)
    self.phab.connect()
    self.phab.update_interfaces()
    self.instance_string = config.phabricator_revision_url

  def notify_harbourmaster(self, buildTargetPHID, success):
    self.phab.harbormaster.sendmessage(buildTargetPHID=buildTargetPHID, type=success)

  def apply_patch(self, id):
    print("ABCD")
    try:
      subprocess.check_output(["git", "-C", self.config.repository_path, "phab", "apply", id])
    except Exception as e:
      raise Exception("git phab application failed: "+e.output)
    print("ABCDEFG")

  def get_id_from_commit_message(self, msg):
    revision_numbers = re.findall(r""+self.instance_string+"/D(\d+)", msg)
    if len(revision_numbers) == 0:
      raise Exception("Revision ID cannot be fetched from commit message")
    return "D"+revision_numbers[-1]
