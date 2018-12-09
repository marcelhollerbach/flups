class Config:
  def __init__(self):
    self.repository_path = "path-to-repository"
    self.repository_patch_origin = "where-master-is-coming-from"
    self.repository_patch_destination = "where-patches-are-going"
    self.ssh_pubkey = "<path-to-pubkey>"
    self.ssh_privkey = "<path-to-privkey>"
    self.ssh_passphrase = 'passphrase to decrypt'
    self.phabricator_url = 'phabricator-url/api/ (THE API PART IS IMPORTANT)'
    self.phabricator_token = "conditor-token"
