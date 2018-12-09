import subprocess

class Workflow:
  def __init__(self, name, targetBuildId, config, repository, phab):
    self.name = name
    self.repository = repository
    self.config = config
    self.targetBuildId = targetBuildId
    self.phab = phab

  #apply the patch from phabricator to the git repository and publish it
  def apply(self):
    self.repository.lock_patch_work(self.name)
    if self.phab.apply_patch(self.name) == False:
      return False
    self.repository.unlock_patch_work(self.name)
    return True

  #message back to phabricator about success or failure
  def finalize(self, success):
    self.repository.dispatch(self.name)
    result = ""
    if success == True:
      result = "success"
    else:
      result = "fail"
    self.phab.notify_harbourmaster(self.targetBuildId, result)
    pass
