#! /bin/bash

PROCESS_NUM=1
TOOL_NAME="weather"
INPUT_QUERY="../queries/output/${TOOL_NAME}/10000_queries.json"
OUTPUT_ANSWER="./output/${TOOL_NAME}/10000_answers_react.jsonl"
DEBUG=1

mkdir output/
mkdir output/${TOOL_NAME}/
mkdir -p output/${TOOL_NAME}/log

OPTS=""
OPTS+=" --tool_name ${TOOL_NAME}"
OPTS+=" --input_query_file ${INPUT_QUERY}"
OPTS+=" --output_answer_file ${OUTPUT_ANSWER}"
OPTS+=" --process_num ${PROCESS_NUM}"
OPTS+=" --debug ${DEBUG}"

CMD="python main_react.py ${OPTS}"

echo ${CMD}
${CMD} 2>&1 | tee output/${TOOL_NAME}/log/$(date +%Y%m%d_%H%M%S).txt