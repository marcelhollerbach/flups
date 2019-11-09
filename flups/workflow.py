class Workflow:
  def __init__(self, name, targetBuildId, config, repository, phab, state):
    self.name = name
    self.repository = repository
    self.config = config
    self.targetBuildId = targetBuildId
    self.phab = phab
    self.state = state

  #apply the patch from phabricator to the git repository and publish it
  def apply(self):
    self.repository.lock_patch_work(self.name)
    self.state.state_string = "Starting to apply "+self.name
    try:
      self.phab.apply_patch(self.name)
    finally:
      self.state.state_string = "Updating origin "+self.name
      self.repository.unlock_patch_work(self.name)
    self.state.state_string = "Going to Idle, we are done with "+self.name

  #message back to phabricator about success or failure
  def finalize(self, success):
    self.repository.dispatch(self.name)
    self.phab.notify_harbourmaster(self.targetBuildId, success)
    pass
