from flask import Flask
from flups.state import State
from flups.config import Config
from flups.repository import Repo
from flups.workflow import Workflow
from flups.phab import Phab
from flask import request

app = Flask(__name__)
config = Config()
repository = Repo(config)
phabricator = Phab(config)
state = State(config, repository, phabricator)

@app.route("/")
def flups():
    return "Current load of requests: "+str(len(state.map))

@app.route("/run", methods=["POST"])
def run():
    id = request.form['buildRevision']
    target_build_phid = request.form['buildTargetPHID']
    workflow = state.get_or_create(id, target_build_phid)
    workflow.apply()
    return ('', 204)

@app.route("/finish", methods=["POST"])
def finish():
    id = request.form['buildRevision']
    workflow = state.dispatch(id)
    workflow.finalize(False)
    return ('', 204)
