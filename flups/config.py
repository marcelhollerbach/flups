import configparser

class Config:
  def __init__(self):
    config = configparser.ConfigParser()
    assert len(config.read('config.ini')) != 0
    #FIXME input validation
    self.repository_path = config["repository"]["path"]
    self.repository_patch_origin = config["repository"]["patch-origin"]
    self.repository_patch_destination = config["repository"]["patch-destination"]
    self.ssh_pubkey = config["git-ssh-connection"]["pub-key"]
    self.ssh_privkey = config["git-ssh-connection"]["priv-key"]
    self.ssh_passphrase = config["git-ssh-connection"]["passphrase"]
    self.phabricator_url = config["phabricator"]["url"]
    self.phabricator_revision_url = config["phabricator"]["revision-url"]
    self.phabricator_token = config["phabricator"]["conduit-token"]
