#!/bin/bash

# this script creates a new virtual env
# and loads the requisite packages 
# to create an app from the PhotoOrganizer.py file
# using py2app

# create a virtual environment in the current directory
python3 -m venv PhotoEnv

# activate the environment
source PhotoEnv/bin/activate

# install dependencies for app
pip install pysimplegui py2app

# create app with py2app
python3 setup.py py2app

# how to zip the file without breaking the symlinks
zip --symlinks -r PhotoOrganizer.app.zip 'dist/Photo Organizer.app'