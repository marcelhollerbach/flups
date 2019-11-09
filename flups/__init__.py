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
    #TODO run this async
    workflow.apply()
    return ('', 204)

@app.route("/finish", methods=["GET"])
def finish():
    commit_hash = request.args.get('sha')
    id = phabricator.get_id_from_commit_message(repository.fetch_commit_message(commit_hash))
    workflow = state.dispatch(id)
    print(request.args.get('state'))
    workflow.finalize(request.args.get('state'))
    return ('', 204)
