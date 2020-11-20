#!/usr/bin/env bash

flake8 \
    . \
    --count \
    --select=E9,F63,F7,F82 \
    --show-source \
    --statistics \
    --exclude '.svn','CVS','.bzr','.hg','.git','__pycache__','.tox','.eggs','*.egg','env'

if [ $? -eq 1 ]
then
    echo "Error: Syntax errors or undefined names."
    exit 1
else
    echo "No errors"
fi
