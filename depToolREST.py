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

# Create app with the desired parameters...
app = create_rest_app(__name__, command='/depTool', internal_app=dt)

if __name__ == '__main__':
    # It is just a tech preview. Properly implemented in e-magyar (emtsv): https://github.com/dlt-rilmta/emtsv !
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':
        from TSVRESTTools.tsvhandler import process
        sys.stdout.writelines(process(sys.stdin, dt))
    else:
        app.run(debug=True)
