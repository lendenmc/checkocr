#!/bin/bash

set -e

set -x

brew update

case "${TOX_ENV}" in
    py27)
        curl -O https://bootstrap.pypa.io/get-pip.py
        sudo python get-pip.py
        ;;
    py32)
        brew upgrade pyenv
        pyenv install 3.2.6
        pyenv global 3.2.6
        ;;
    y33)
        brew upgrade pyenv
        pyenv install 3.3.6
        pyenv global 3.3.6
        ;;
    py34)
        brew upgrade pyenv
        pyenv install 3.4.2
        pyenv global 3.4.2
        ;;
    pypy)
        brew upgrade pyenv
        pyenv install pypy-2.4.0
        pyenv global pypy-2.4.0
        ;;
    pypy3)
        brew upgrade pyenv
        pyenv install pypy3-2.4.0
        pyenv global pypy3-2.4.0
        ;;
esac
pyenv rehash

sudo pip install virtualenv
virtualenv ~/.venv
source ~/.venv/bin/activate
pip install tox coveralls