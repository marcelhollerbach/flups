import configparser

class Config:
  def __init__(self):
    config = configparser.ConfigParser()
    config.read('example.ini')

    self.repository_path = config["repository"]["path"]
    self.repository_patch_origin = config["repository"]["patch-origin"]
    self.repository_patch_destination = config["repository"]["patch-destination"]
    self.ssh_pubkey = config["git-ssh-connection"]["pub-key"]
    self.ssh_privkey = config["git-ssh-connection"]["priv-key"]
    self.ssh_passphrase = config["git-ssh-connection"]["passphrase"]
    self.phabricator_url = config["phabricator"]["url"]
    self.phabricator_token = config["phabricator"]["conduit-token"]
