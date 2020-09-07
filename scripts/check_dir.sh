#!/bin/bash
DEFAULT_EXT="*.wsdl"
VERBOSE=0
ALIGN=0
usage=NOK
isEqual=1

help="
$0 [-h] [-v] [-f <file_name> | -e ext_files] <source-path-dir> <destination-path-dir> \n
-h : help
-v : verbose
-a : align files
-f : file name - useful if you to check differce among a single and specific file
-e : file extensions [Default : *.wsdl] use to find all files with a specific extension into  <source-path-dir>  and <destination-path-dir> folders
<source-path-dir> : path where script start to find files with ext_files to compare vs files (with same name) present into <destination-path-dir>
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

        -v|--vervose)
            VERBOSE=1
            shift
        ;;

        -a|--align)
            ALIGN=1
            shift
        ;;
        -vv|--very-vervose)
            VERBOSE=2
            shift
        ;;

        -f|--file)
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                MY_FILE=$2
                shift 2
            else
                echo "Error1: Argument for $1 is missing" >&2
                exit 1
            fi
        ;;

        -e|--ext)
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                DEFAULT_EXT="*."$2
                shift 2
            else
                echo "Error2: Argument for $1 is missing" >&2
                exit 1
            fi
        ;;

        *) # preserve positional arguments
            # echo "$# $@"
            if [ $# -eq 2 ] && [ -n "$2" ] && [ -n "$1" ]; then
                SRC=$1
                DST=$2
                usage=OK
            else
                usage=NOK
            fi
            break
        ;;

    esac
done


if [ "$usage" = "OK" ]
then
    echo -n "Start..."
    find $SRC -name $DEFAULT_EXT | egrep -v $DST | xargs -L1 -I{} basename "{}" | sort | uniq > file1.txt
    find $DST -name $DEFAULT_EXT | xargs -L1 -I{} basename "{}" | sort | uniq > file2.txt

    comuni=`comm -12 <(sort file1.txt) <(sort file2.txt)`

    if [ $VERBOSE == 1 ] && [ -z "$MY_FILE" ]; then

        echo ""
        # echo ">>>>>>>>>>>>>>>>>>>>"
        echo ">>> common files >>>"
        # echo ">>>>>>>>>>>>>>>>>>>>"
        comm -12 <(sort file1.txt) <(sort file2.txt)
        echo "Done !"

        # echo ">>>>>>>>>>>>>>>>>>>>"
        res=`comm -13 <(sort file1.txt) <(sort file2.txt)`
        res1=${res//[[:blank:]]/}
        echo ">>> only into $DST possibly DELETED files -$res1- !!!"
        # echo ">>>>>>>>>>>>>>>>>>>>"
        comm -13 <(sort file1.txt) <(sort file2.txt)
        echo "Done !"

        # echo ">>>>>>>>>>>>>>>>>>>>"
        res=`comm -23 <(sort file1.txt) <(sort file2.txt) | wc -l`
        res2=${res//[[:blank:]]/}
        echo ">>> only into $SRC possibly NEW files -$res2-"
        # echo ">>>>>>>>>>>>>>>>>>>>"
        comm -23 <(sort file1.txt) <(sort file2.txt)
        echo "Done !"

        # echo ">>>>>>>>>>>>>>>>>>>>"
        echo ">>> DEFAULT filter $DEFAULT_EXT applied"
        # echo ">>>>>>>>>>>>>>>>>>>>"

        if [ $res2 != "0" ] || [ $res1 != "0" ]; then
            echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            echo "!!! Error resolve before manually new/delete files !!!!"
            echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            exit 1
        fi

    fi

    # remove TMP file
    # rm -f file1.txt file2.txt

    # restrict to ONE file
    if [ ! -z "$MY_FILE" ]; then
        comuni=($MY_FILE)
    fi

    # Files differences ...
    for entry in $comuni
    do
        # echo $entry1

        file1=`find $SRC -name $entry | egrep -v $DST | head -n 1`
        # file2=`find $DST -name $entry | head -n 1`

        # echo "File $entry"

        # num1=`find $SRC -name $entry | wc -l`
        # echo "in $SRC : ${num1}"
        # find $SRC -name $entry

        # num2=`find $DST -name $entry | wc -l`
        # echo "in $DST : ${num2}"
        # find $DST -name $entry

        multipli=`find $DST -name $entry`

        for file2Replicate in $multipli
        do
            # echo "diff $file1 $file2"
            num_diff=`diff $file1 $file2Replicate -U 0 | grep -v ^@ | wc -l`
            differenze=${num_diff//[[:blank:]]/}

            if [ $differenze != "0" ]; then
                isEqual=0
            fi

            if [ $VERBOSE == 1 ]; then
                echo "differences for $entry are : ${differenze}"
            fi

            if [ $VERBOSE == 2 ]; then
                echo -n "differences ${differenze} : $file1 vs $file2Replicate "
                if [ $differenze == "0" ]; then
                    echo "equal :)"
                else
                    echo "DIFFERENT :( !!!"
                fi
                diff $file1 $file2Replicate
            fi

            # align
            if [ $ALIGN == 1 ] && [ $differenze != "0" ]; then
                echo "cp $file1 $file2Replicate"
                cp $file1 $file2Replicate
            fi
        done

    done

    if [ $isEqual == 1 ]; then
        echo "$SRC and $DST are equal."
        # exit 0
    else
        echo "$SRC and $DST are different !!!"
        # exit 1
    fi
    echo "Done !"
    echo "*******************************************************"
    echo "***               ALIGN COMPLETE                    ***"
    echo "*******************************************************"

else
    echo ""
    echo "Bad usage !!!"
    echo "$help"
    echo ""
fi
