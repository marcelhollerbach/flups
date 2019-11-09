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
state = State(repository, phabricator)

@app.route("/")
def flups():
    return "Current load of requests: "+str(len(state.map))+"\n Currently: "+state.state_string

@app.route("/run", methods=["GET"])
def run():
    key = request.args.get('buildRevision')
    state.schedule_apply(key)
    return ('', 204)

@app.route("/finish", methods=["GET"])
def finish():
    phab_state = ""
    commit_hash = request.args.get('sha')
    new_state = request.args.get('state')

    if new_state == "success":
        phab_state = "pass"
    elif new_state == "failure":
        phab_state = "fail"
    elif new_state == "error":
        phab_state = "fail"
    elif new_state == "pending":
        phab_state = ""
    else:
        raise Exception("not understood state "+phab_state)

    if phab_state != "":
        key = phabricator.get_id_from_commit_message(repository.fetch_commit_message(commit_hash))
        state.schedule_phabnotify(key, new_state)
    return ('', 204)
