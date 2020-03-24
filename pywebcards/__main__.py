#!/usr/bin/python3
from . import app

app.debug = True
app.run(
    # Threading must be enabled for the turn based multiplayer to send synchronous status updates to all players
    threaded=True,
    # I didn't bother trying to entirely understand it, but inotify reloader fails when importing from current directory.
    # https://github.com/pallets/flask/issues/1246
    # https://github.com/pallets/werkzeug/issues/461
    #
    # It seems no one wants to actually fix this.
    # The inotify reloader tends to get in my way more than it helps though, so I'm just going to disable it.
    use_reloader=False,
)
