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
    self.phab.apply_patch(self.name)
    self.repository.unlock_patch_work(self.name)

  #message back to phabricator about success or failure
  def finalize(self, success):
    self.repository.dispatch(self.name)
    self.phab.notify_harbourmaster(self.targetBuildId, success)
    pass
