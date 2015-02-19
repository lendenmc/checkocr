#!/bin/bash

set -e

set -x

if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi

source ~/.venv/bin/activate

tox -e $TOX_ENV