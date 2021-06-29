#!/usr/bin/env bash

clear

echo -e "⚙️  ✅ Testing this code...\n"
pipenv run coverage run -m pytest
pipenv run coverage report -m --omit="*_test.py,*__init__.py,src/app.py"
