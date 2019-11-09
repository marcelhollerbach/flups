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
    return "Current load of requests: "+str(len(state.map))+"\n Currently: "+state.state_string

@app.route("/run", methods=["GET"])
def run():
    key = request.args.get('buildRevision')
    state.schedule_apply(key, target_build_phid)
    return ('', 204)

@app.route("/finish", methods=["GET"])
def finish():
    commit_hash = request.args.get('sha')
    state = request.args.get('state')
    key = phabricator.get_id_from_commit_message(repository.fetch_commit_message(commit_hash))
    state.schedule_phabnotify(key, state)
    return ('', 204)
