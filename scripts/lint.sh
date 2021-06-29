#!/usr/bin/env bash

echo -e " ✅ Linting code into this python app...\n"
pipenv run pylint -v src
