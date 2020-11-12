#!/bin/bash


# lsof -i :8080 | grep node | cut -f 5 -d ' ' | xargs kill -9
BUILD=0
RUN=0
usage=NOK
SERVICE=0

help="
$0 [-h] [-b] -r <SERVICE_NAME> \n
-h : help
-b : build spec from WSDL
-r : run local documentation for service <SERVICE_NAME> : allowed services {nodeForPa,nodeForPsp,paForNode,pspForNode}
"

# Check parameter
while (( "$#" )); do
    case "$1" in
        -h|--help)
            echo ""
            echo "Usage :"
            echo "$help"
            echo ""
            exit 0
        ;;

        -b|--build)
            BUILD=1
            shift
        ;;

        -r|--run)
            if [[ "$2" =~ ^(nodeForPa|nodeForPsp|paForNode|pspForNode)$ ]]; then
                RUN=$1
                SERVICE=$2
                shift 1
            else
                echo "Error: Argument for '$2' is no allowed" >&2
                exit 1
            fi        
        ;;

        *) # preserve positional arguments
            # echo "$# $@"
            usage=OK
            break
        ;;        

    esac
done


if [ "$usage" = "OK" ]
then
    echo "Start...$BUILD"
    CURR_DIR=$PWD

    if [ $BUILD == 1 ] ; then
        echo -n "Build..."
        rm -rf ./generator/out/*.yamml
        rm -rf ./api-definitions/openapi/*.yaml
        cd generator && yarn install && yarn build
    fi

    echo "OpenSpec..."

    cd $CURR_DIR/api-definitions/openapi
    ./add_snippet.sh $1_Service.yaml
    cd ..
    npm install && npm run $1_Service &
    cd $CURR_DIR

    echo "Done !"


else
    echo ""
    echo "Bad usage !!!"
    echo "$help"
    echo ""
fi
