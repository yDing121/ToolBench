#! /bin/bash

MODEL="gpt-3.5-turbo"
MAX_TOKENS=2048
FREQUENCY_PENALTY=0
PRESENCE_PENALTY=0
BEST_OF=3
STOP=None
PARALLEL=1
TOTAL_NUM=1000
TOOL_NAME="weather"
LANGUAGE="en"

OPTS=""
OPTS+=" --model ${MODEL}"
OPTS+=" --max_tokens ${MAX_TOKENS}"
OPTS+=" --frequency_penalty ${FREQUENCY_PENALTY}"
OPTS+=" --presence_penalty ${PRESENCE_PENALTY}"
OPTS+=" --best_of ${BEST_OF}"
OPTS+=" --stop ${STOP}"
OPTS+=" --parallel ${PARALLEL}"
OPTS+=" --total_num ${TOTAL_NUM}"
OPTS+=" --tool_name ${TOOL_NAME}"
OPTS+=" --language ${LANGUAGE}"
# OPTS+=" --cold_start"

CMD="python incontext.py ${OPTS}"

echo ${CMD}
${CMD} 2>&1 | tee generate_${TOOL_NAME}_queries.log
python dedpulication.py --file_path output/${TOOL_NAME}/${TOTAL_NUM}_queries.json
