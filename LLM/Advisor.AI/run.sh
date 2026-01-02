
#!/bin/bash
arg=${1}
DATE_TIME=`date '+%Y-%m-%d %H:%M:%S'`


build() {
    printf "\n ----------------------------------------------------------------  "
    printf "\n       ------------ Build, compile SRC code------------  "
    printf "\n ----------------------------------------------------------------  \n"

    # install dependencies
    pip3 install -r requirements.txt

    # compile source code
    python3 -m compileall -l ./src/
}

info(){
    printf "Python version: $(python3 --version)\n"
    printf "pip version: $(pip3 --version)\n"
    printf "Python path: $(which python3)\n"
    printf "pip3 path: $(which pip3)\n"
}






# Check for 1 argument
if [ $# -ne 1 ]; then
  echo "Error: This script requires exactly 1 arguments."
  echo "    ./runs.sh <build | run | delete> "
fi
# -z option with $1, if the first argument is NULL. Set to default
if  [[ -z "$1" ]] ; then # check for null
    echo "User action is NULL, setting to default INSTALL"
    arg='RUN'
fi

# -n string - True if the string length is non-zero.
if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"
    
    if [[ "BUILD" == "${arg}" ]] ; then   # Download & install 
        info
        build
    elif [[ "INFO" == "${arg}" ]] ; then   
        info
    fi
fi



printf "\n ----------------------------------------------------------------  "

printf "\n***** [END] TS: $(date +"%Y-%m-%d %H:%M:%S") \n\n"