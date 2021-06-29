#!/usr/bin/env bash

clear

echo -e " 📺 Starting as watch mode the running script...\n"
echo -e " 💻 Watching all .py files on src/, excepting for test files *_test.py\n"

pipenv run watchgod --verbosity 1 src.main src/
