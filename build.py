from distutils.core import setup
import py2exe
from flask import *
import flask_cors

setup(console = ['grader.py'])
