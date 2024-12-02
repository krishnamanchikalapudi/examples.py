arg=${1}
clear
export JF_HOST="psazuse.jfrog.io"  JFROG_RT_USER="krishnam" JFROG_CLI_LOG_LEVEL="DEBUG"
export JF_RT_URL="https://${JF_HOST}" RT_REPO_DOCKER_VIRTUAL="krishnam-docker-virtual"
export BUILD_NAME="frogml-churn-predict" BUILD_ID="cmd.dkr.$(date '+%Y-%m-%d-%H-%M')" 
export DOCKER_MANIFEST="list.manifest-${BUILD_ID}.json"  DOCKER_SPEC_BUILD_PUBLISH="dockerimage-file-details-${BUILD_ID}"

DATE_TIME=`date '+%Y-%m-%d %H:%M:%S'`

## Health check
printf "\n\n*** RT ${JF_RT_URL} status is $(jf rt ping --url=${JF_RT_URL}/artifactory) \n"

containerId=`docker container ls -a | grep ${BUILD_NAME} | awk '{print $1}'`
imageId=`docker image ls -a | grep ${BUILD_NAME} | awk '{print $3}'`

clean() {
    echo "\n**** [START] DOCKER CLEAN at $(date '+%Y-%m-%d-%H-%M') ****\n" 
    printf "Cleaning containers and image-ids from local \n"
    # docker rmi -f ${imageId}  
    docker image prune -a -f --filter "until=1h"
    docker container prune -f --filter "until=1h"
    docker system prune -f --filter "until=1h"
    sleep 3
    docker rmi -f $(docker images -aq)
    echo "\n**** [END] DOCKER CLEAN at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}
srcCompile() {
    echo "\n**** [START] SRC - COMPILE at $(date '+%Y-%m-%d-%H-%M') ****\n"
    pip3 install -r requirements.txt

    python3 -m compileall -l -f ./src  # ref: https://docs.python.org/3/library/compileall.html#module-compileall

    python3 -m unittest -v tests/PredictApiTests.py # ref: https://docs.python.org/3/library/unittest.html#module-unittest

    echo "\n**** [END] SRC - COMPILE at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}
apiTest() {
    echo "\n**** [START] API - TEST at $(date '+%Y-%m-%d-%H-%M') ****\n"
    flask --app src/PredictApi.py run --port=5000 --debug & 
    sleep 3

    tests

    echo "\n* Shutdown FLASK service" 
    lsof -ti:5000 | xargs kill -9    
    sleep 3
    echo "\n**** [END] API - TEST at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}
tests(){ 
    sleep 1 && echo "\n\n"
    curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:5000/"
    
    sleep 1 && echo "\n"
    export GEN_RANDOM_NUMBER="$(date '+%Y%m%d%H%M%S')"
    curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:5000/${GEN_RANDOM_NUMBER}"
}
imageBuild() {
    echo "\n**** [START] DOCKER BUILD at $(date '+%Y-%m-%d-%H-%M') ****\n" 
    echo " BUILD_NAME: $BUILD_NAME \n BUILD_ID: $BUILD_ID \n JFROG_CLI_LOG_LEVEL: $JFROG_CLI_LOG_LEVEL \n RT_REPO_DOCKER_VIRTUAL: $RT_REPO_DOCKER_VIRTUAL \n"

    ## Docker: config
    # export DOCKER_PWD="<GET_YOUR_OWN_KEY>" 
    echo "\n**** Docker: login ****\n" 
    docker login ${JF_HOST} -u krishnam -p ${DOCKER_PWD}

    ### Docker: Create image and push
    echo "\n**** Docker: build image ****\n"
    # docker image build -f Dockerfile -t frogml-churn-predict:latest .
    docker image build -f Dockerfile -t ${JF_HOST}/${RT_REPO_DOCKER_VIRTUAL}/${BUILD_NAME}:${BUILD_ID} --output=type=image . 

    docker image ls 

    ### Docker Push image
    echo "\n**** Docker: jf push ****\n"
    jf docker push ${JF_HOST}/${RT_REPO_DOCKER_VIRTUAL}/${BUILD_NAME}:${BUILD_ID} --build-name=${BUILD_NAME} --build-number=${BUILD_ID} --detailed-summary=true

    echo "\n\n**** [END] DOCKER BUILD at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}
imageRun() {
    echo "\n\n**** [START] DOCKER RUN at $(date '+%Y-%m-%d-%H-%M') ****\n" 
    printf "\n -------- Downloading container: ${BUILD_NAME} -------- \n "
    docker pull ${JF_HOST}/${RT_REPO_DOCKER_VIRTUAL}/${BUILD_NAME}:${BUILD_ID}

    # docker run -d --name frogml-churn-predict -p 5000:5000 frogml-churn-predict:latest
    docker run -d --name ${BUILD_NAME} -p 5000:5000 ${JF_HOST}/${RT_REPO_DOCKER_VIRTUAL}/${BUILD_NAME}:${BUILD_ID}

    sleep 15
    docker logs -f ${BUILD_NAME} &
    
    sleep 5
    echo "\n **** Service response: $(curl -X GET http://localhost:5000/)  \n"   

    echo "\n\n**** [END] DOCKER RUN at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}
imageStop() {
    echo "\n\n**** [START] DOCKER STOP at $(date '+%Y-%m-%d-%H-%M') ****\n" 
    printf "container: ${BUILD_NAME} -------- \n "
     # docker container stop ${docker container ls -a | grep postgres | awk '{print $1}'}
     docker stop $BUILD_NAME -t 0
     sleep 5
     docker rm -f $BUILD_NAME

     echo "\n\n**** [END] DOCKER STOP at $(date '+%Y-%m-%d-%H-%M') ****\n" 
}

# -z option with $1, if the first argument is NULL. Set to default
if  [[ -z "$1" ]] ; then # check for null
    echo "User action is NULL, setting to default RESTART"
    arg='START'
fi

# -n string - True if the string length is non-zero.
if [[ -n $arg ]] ; then
    arg_len=${#arg}
    # uppercase the argument
    arg=$(echo ${arg} | tr [a-z] [A-Z] | xargs)
    echo "User Action: ${arg}, and arg length: ${arg_len}"

    if  [[ "CLEAN" == "${arg}" ]] ; then # Clean 
        clean
    elif [[ "SRC" == "${arg}" ]] ; then   # SRC compile
        srcCompile
    elif [[ "API-TEST" == "${arg}" ]] ; then   # API-TEST
        apiTest
    elif [[ "BUILD" == "${arg}" ]] ; then   # Download & start 
        imageBuild
    elif [[ "START" == "${arg}" ]] ; then   # Download & start 
        imageRun
    elif [[ "START" == "${arg}" ]] ; then   # stop 
        imageStop
    fi
fi
