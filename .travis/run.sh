#!/bin/bash

set -e

set -x

eval "$(pyenv init -)"

source ~/.venv/bin/activate

tox -e $TOX_ENV