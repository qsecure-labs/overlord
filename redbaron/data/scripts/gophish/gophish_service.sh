#!/bin/bash

GOPHISH_LOG_FILE=gophish.log
GOPHISH_ERR_FILE=gophish.err

check_bin_path() {
    if [[ -z "$GOPHISH_BIN_PATH" ]]; then
        exit 1
    fi
}

check_log_path() {
    if [[ -z "$GOPHISH_LOG_PATH" ]]; then
        exit 2
    fi
}

create_new_log_err() {
    GOPHISH_STAMP=`date +%Y%m%d%H%M%S-%N`
    if [[ -e $GOPHISH_LOG_PATH$GOPHISH_LOG_FILE ]]; then
        mv $GOPHISH_LOG_PATH$GOPHISH_LOG_FILE $GOPHISH_LOG_PATH$GOPHISH_LOG_FILE-$GOPHISH_STAMP
    fi
    
    if [[ -e $GOPHISH_LOG_PATH$GOPHISH_ERR_FILE ]]; then
        mv $GOPHISH_LOG_PATH$GOPHISH_ERR_FILE $GOPHISH_LOG_PATH$GOPHISH_ERR_FILE-$GOPHISH_STAMP
    fi
    
    touch $GOPHISH_LOG_PATH$GOPHISH_LOG_FILE
    touch $GOPHISH_LOG_PATH$GOPHISH_ERR_FILE
}

launch_gophish() {
    cd $GOPHISH_BIN_PATH
    ./gophish >> $GOPHISH_LOG_PATH$GOPHISH_LOG_FILE 2>> $GOPHISH_LOG_PATH$GOPHISH_ERR_FILE
}

check_bin_path
check_log_path
create_new_log_err
launch_gophish