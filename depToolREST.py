#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

from TSVRESTTools.common import create_rest_app

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'deptoolpy'))  # Needed to be able to use git submodule...
from deptoolpy import DepToolPy

# Initialize tagger as wanted...
dt = DepToolPy()

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
# Create app with the desired parameters...
app = create_rest_app(__name__, command='/depTool', internal_app=dt)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        from TSVRESTTools.tsvhandler import process
        sys.stdout.writelines(process(sys.stdin, dt))
    else:
        app.run(debug=True)
