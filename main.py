#!/usr/bin/env python2

import utils
import json
import argparse

def main():    
    ## Load all the engines
    alertEngines = utils.loadEngines("engines/alerts")
    actionEngines = utils.loadEngines("engines/actions")

    ## Load ES Connection config
    connections = json.load(open("connections.json"))
    conns = connections["nodes"]

    ## Load configured alerts
    alerts = json.load(open("alerts.json"))

    ## Process alert configs
    for config in alerts["alerts"]:
        alert = utils.Alert(config)
        alertEC = config["AlertEngines"]
        for engine in alertEC: ## Configured alerts
            if engine["name"] in alertEngines:
                alert.addAlertEngine(alertEngines[engine["name"]].init(conns, engine["args"]))
            else:
                print "Warning: Unknown alert engine", engine["name"]
        actionEC = config["ActionEngines"]
        for engine in actionEC: ## Configured actions
            if engine["name"] in actionEngines:
                alert.addActionEngine(actionEngines[engine["name"]].init(engine["args"]))
            else:
                print "Warning: Unknown action engine", engine["name"]
        alert.check()



main()
