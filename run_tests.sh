#!/usr/bin/env bash
$KB_SDK_BIN/kb-sdk compile GenomeAnnotationAPI.spec --py --pysrv --out lib/GenomeAnnotationAPI
$KB_SDK_BIN/kb-sdk test
cp .coveragerc test_local/workdir/.coveragerc
docker run -v "$(pwd)"/test_local/workdir:/kb/module/work -e "SDK_CALLBACK_URL=$1" test/genomeannotationapi:latest test