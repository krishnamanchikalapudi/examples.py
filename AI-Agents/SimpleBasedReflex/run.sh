#!/bin/bash
arg=${1}
DATE_TIME=`date '+%Y-%m-%d %H:%M:%S'`
NAMESPACE="AIAgent-simple-reflex"
alias k=kubectl

py-build() {
    pip install -r requirements.txt
}

py-test() {
    pytest unittest/reflex_agent_tests.py -v 
}

py() {
    py-build && py-run && py-test
}
docker() {
    docker build -t krishnamanchikalapudi/reflex-agent .
    docker run -it --rm krishnamanchikalapudi/reflex-agent
}

# Check for 1 argument
if [ $# -ne 1 ]; then
  echo "Error: This script requires exactly 1 arguments."
  echo "    ./run.sh <build | run | test | kill> "
fi
# -z option with $1, if the first argument is NULL. Set to default
if  [[ -z "$1" ]] ; then # check for null
    echo "User action is NULL, setting to default BUILD"
    arg='BUILD'
fi

# -n string - True if the string length is non-zero.
if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"
    
    if [[ "BUILD" == "${arg}" ]] ; then   # Download & install 
        py-build
    elif [[ "RUN" == "${arg}" ]] ; then   # delete 
        py-run
    elif [[ "KILL" == "${arg}" ]] ; then   # Info 
        py-kill
    elif [[ "TEST" == "${arg}" ]] ; then   # Info 
        py-test
    elif [[ "PY" == "${arg}" ]] ; then   # Info 
        py
    fi
fi

printf "\n ----------------------------------------------------------------  "
