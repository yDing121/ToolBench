call conda.bat activate ToolBench
start cmd /c call ./run_helper/run_tool_server.bat
start cmd /c call ./run_helper/query_from_seed.bat
pause