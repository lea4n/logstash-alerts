import os
import time
import re
import imp
from os.path import join

def parse_time(time_str):
    regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

def loadEngines(directory):
    """import engines from a given directory"""
    engines = {}
    cwd = os.getcwd()
    files = [(x.split(".")[0], join(cwd,directory,x)) for x in os.listdir(join(cwd, directory)) if ((x.split(".")[1] == "py") and (x[0] != "_"))]
    for x in files:
        engines[x[0]] = imp.load_source(x[0],x[1])
    return engines

class Alert:
    def __init__(self, config):
        self.name = config["name"]
        self.config = config
        self.AlertEngines = []
        self.ActionEngines = []
        indexTimestamp = config["index"].split("+")[-1]
        query = config["query"]
    def addAlertEngine(self, engine):
        self.AlertEngines.append(engine)
    def addActionEngine(self, engine):
        self.ActionEngines.append(engine)
    def check(self):
        for alert in self.AlertEngines:
            alert.run(self.config)
