#!/usr/bin/env bash

clear

echo -e "⚙️ Testing the code into this python app...\n"
pipenv run python -m pytest \
    -s \
    --verbose \
    --last-failed \
    --new-first \
    --failed-first \
