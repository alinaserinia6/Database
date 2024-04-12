#! /bin/bash

case $( uname -s ) in
    Linux) sudo apt install python3-termcolor;;
    *)     pip install termcolor;;
esac
