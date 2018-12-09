from flups.workflow import Workflow

class State:
  def __init__(self, config, repository, phab):
    self.map = {}
    self.config = config
    self.repository = repository
    self.phab = phab

  def get_or_create(self, key, targetBuildId):
    if not key in self.map:
      self.map[key] = Workflow(key, targetBuildId, self.config, self.repository, self.phab)
    return self.map[key]

  def dispatch(self, key):
    workflow = self.map[key]
    del self.map[key]
    return workflow;
