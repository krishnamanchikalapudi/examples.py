# Generic management tasks
# Usage:
# make        # compile all binary
# make clean  # remove ALL binaries and objects

init:
    pip3 -V
    python3 -V

clean:
    @echo "cleaning generated folders..."
    rm -rf build dist src.egg-info

install:
    @echo "installing python libraries..."
    pip3 install -r requirements.txt

compile:
    @echo "compiling python source code..."
    python3 -m compileall -l ./src/

test:
    @echo "executing python test suite..."
    py.test tests

all: init clean install compile

.DEFAULT_GOAL := all
