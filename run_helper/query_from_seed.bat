echo "Generating queries from seeds..."
cd ./data-generation/queries
:: Edit stuff here
python incontext.py --tool_name weather2 --total_num 10
:: pause