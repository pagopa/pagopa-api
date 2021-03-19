#!/bin/bash

function clone_check_common_xml () {
    echo -n "    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> $1"
    VERS=`curl -k $2 > tmp_.json && python ./scripts/read_vers.py tmp_.json c`
    rm -rf "$1vers_"$VERS
    mkdir "$1vers_"$VERS
    cd "$1vers_"$VERS
    git clone https://github.com/pagopa/pagopa-nodo4-common-xml.git
    cd pagopa-nodo4-common-xml
    git checkout "v"$VERS > /dev/null 2>&1
    echo $VERS
    cd ../..
    ./scripts/check_dir.sh -v . "$1vers_"$VERS
    chk_wsdl=$?
    echo "WSDL ${chk_wsdl}"
    ./scripts/check_dir.sh -v -e xsd . "$1vers_"$VERS
    chk_xsd=$?
    echo "XSD ${chk_xsd}"
    # rm -rf "$1vers_"$VERS
    return $((chk_wsdl+chk_xsd))
}

# store arguments in a special array
args=("$@")
VERSIONS=("SIT" "UAT" "PROD")
idx=0
READLINE=false

filename="./scripts/resources/vers.txt"
filenameNew="./scripts/resources/vers_.txt"
ORA=`date +"%Y-%m-%d %T"`
echo $ORA >> "$filenameNew"
DIFFERENT=0

while read line; do
    if [ "$READLINE" = true ] ; then
        VERS=`curl -k ${args[${idx}]} > tmp_.json && python ./scripts/read_vers.py tmp_.json c`
        if [ $line != $VERS ]; then
            #     echo ${VERSIONS[${idx}]} "UGUALI"
            # else
            #     echo ${VERSIONS[${idx}]} "DIVERSI"
            DIFFERENT=1;
        fi
        echo $VERS >> "$filenameNew"
        ((idx++))
    fi
    READLINE=true
done < $filename

cp $filenameNew $filename
rm -f $filenameNew

echo $DIFFERENT

# clone_check_common_xml "SIT" $1 /dev/null 2>&1
# resS=$?
# echo "SIT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> "$resS

clone_check_common_xml "UAT" $2 /dev/null 2>&1
resU=$?
echo "UAT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> "$resU

# clone_check_common_xml "PROD" $3 /dev/null 2>&1
# resP=$?
# echo "PROD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> "$resP

