from flups.workflow import Workflow
from concurrent.futures import ThreadPoolExecutor

def async_applying_of_workflow(workflow):
  workflow.apply()

class State:
  def __init__(self, config, repository, phab):
    self.map = {}
    self.config = config
    self.repository = repository
    self.phab = phab
    #always keep that 1 here, more cannot work because we need to lock the repository
    self.executor = ThreadPoolExecutor(max_workers=1)
    self.state_string = "Nothing there yet."

  def get_or_create(self, key):
    if not key in self.map:
      self.map[key] = Workflow(key, self.config, self.repository, self.phab, self)
    return self.map[key]

  def schedule_apply(self, key):
    #FIXME we should check that key and targetBuildId belong to each other
    workflow = self.get_or_create(key)
    self.executor.submit(async_applying_of_workflow, workflow)

  def schedule_phabnotify(self, key, state):
    if not key in self.map:
      raise Exception("Revision "+key+" currently not found")
    workflow = self.map[key]
    del self.map[key]
    workflow.finalize(state)
