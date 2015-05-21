#!/usr/bin/env python
# this runs the app in an interactive python shell

import os
import readline
from pprint import pprint


from flask import *
from flaskApp import *

os.environ['PYTHONINSPECT'] = 'True'
