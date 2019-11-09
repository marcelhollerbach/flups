from pygit2 import Repository
from pygit2 import RemoteCallbacks
from pygit2 import GIT_CREDTYPE_USERPASS_PLAINTEXT
from pygit2 import Username, UserPass, Keypair
from pygit2 import credentials
import threading

class MyRemoteCallback (RemoteCallbacks):
    def __init__(self, config):
      self.config = config
      self.count = 0

    def credentials(self, url, username_from_url, allowed_types):
        pubkey = self.config.ssh_pubkey
        privkey = self.config.ssh_privkey
        passphrase = self.config.ssh_passphrase
        if self.count > 5:
          raise Exception("5 times asking for credentials, looks like auth error")
        else:
          self.count = self.count + 1
        return Keypair(username_from_url, pubkey, privkey, passphrase)

class Repo:
  def __init__(self, config):
    self.repo = Repository(config.repository_path)
    self.config = config
    self.lock = threading.Lock()
    master_ref = self.repo.lookup_reference("refs/heads/master")
    self.repo.checkout(master_ref)
    self.cred = MyRemoteCallback(config)

  def lock_patch_work(self, id):
    self.lock.acquire(True)
    try:
      #first lets update master
      self.repo.remotes[self.config.repository_patch_origin].fetch()
      #get the latest master
      master_ref = self.repo.branches.remote[self.config.repository_patch_origin+'/master']
      #In case the branch exists, delete it
      if id in self.repo.branches:
        self.repo.branches.delete(id)
      #create a new branch
      local = self.repo.branches.local.create(id, master_ref.peel())
      #finally switch over
      self.repo.checkout(local)
    except Exception as e:
      self.lock.release()
      raise e

  def unlock_patch_work(self, id):
    try:
      self.repo.remotes[self.config.repository_patch_destination].push(["+refs/heads/"+id], callbacks=self.cred)
      master_ref = self.repo.branches.remote[self.config.repository_patch_origin+'/master']
      self.repo.checkout(master_ref)
    finally:
      self.lock.release()

  def dispatch(self, id):
    #FIXME also delete on the remote
    self.repo.branches.delete(id)

  def fetch_commit_message(self, chash):
    obj = self.repo.get(chash)
    return obj.message

