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

@app.route("/run", methods=["GET"])
def run():
    id = request.args.get('buildRevision')
    target_build_phid = request.args.get('buildTargetPHID')
    workflow = state.get_or_create(id, target_build_phid)
    workflow.apply()
    return ('', 204)

@app.route("/finish", methods=["GET"])
def finish():
    available_options = ['pass', 'fail', 'work']
    id = request.args.get('buildRevision')
    success = request.args.get('buildSuccess')
    if not success in available_options:
        return (''+success+' has to be either pass, fail or work', 400)
    workflow = state.dispatch(id)
    workflow.finalize(success)
    return ('', 204)
