#!/bin/bash

source .env

# Mac/Linux activate environment
source .venv

# Install dependencies
pip install -r requirements.txt

# Go to Tests Folder and run tests GUI
sbase gui
