# coding:utf-8
"""
Data preprocessing
"""
import argparse
import json
import os

import jsonlines

parser = argparse.ArgumentParser()
parser.add_argument('--tool_mode', type=str, default="single", required=True, help='Single tool data or multi tools data. Should be single or multi.')
parser.add_argument('--tool_data_path', type=str, default="", required=True, help='Original tool data path.')
parser.add_argument('--output_path', type=str, default="", required=True, help='Preprocessed tool data output path.')
args = parser.parse_args()


def preprocess_single(tool_data_path):
    out_list = []
    print("this works")

    # # Writer output here ----
    # writer = open(os.path.join(args.output_path, "weather2.json"), "a+")
    with jsonlines.open(tool_data_path) as reader:
        for entry in reader:
            data_dict = entry.copy()

            prompt = data_dict["prompt"]
            query = data_dict["query"]
            chains = data_dict["chains"]
            scratch_pad = ""

            for step_cnt, chain in enumerate(chains):
                thought = chain["thought"]
                action = chain["action"]
                action_input = chain["action_input"]
                observation = chain["observation"]
                inputs = prompt.replace("{input}", query).replace("{agent_scratchpad}", scratch_pad)
                target = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}\n"
                scratch_pad += (target + f"Observation: {observation}\n")
                tmp_dict = {
                    "id": f"STEP {step_cnt}: " + query,
                    "conversations":[
                        {
                            "from": "human",
                            "value": inputs
                        },
                        {
                            "from": "gpt",
                            "value": target
                        }
                    ]
                }
                out_list.append(tmp_dict)

            inputs = prompt.replace("{input}", query).replace("{agent_scratchpad}", scratch_pad)
            answer = data_dict["answer"]
            target = f"Thought: I have got enough information\nFinal Answer:{answer}\n"

            tmp_dict = {
                "id": f"STEP {step_cnt} WITH API: " + query,
                "conversations":[
                    {
                        "from": "human",
                        "value": inputs
                    },
                    {
                        "from": "gpt",
                        "value": target
                    }
                ]
            }
            out_list.append(tmp_dict)
        json.dump(out_list, open(os.path.join(args.output_path, "weather2.json"), "w"), indent=4, ensure_ascii=False)


    # data_dicts = json.load(open(tool_data_path, "r"))
    # for data_dict in data_dicts:
    #     prompt = data_dict["prompt"]
    #     query = data_dict["query"]
    #     chains = data_dict["chains"]
    #     answer = data_dict["answer"]
    #     scratch_pad = ""
    #     for step_cnt, chain in enumerate(chains):
    #         thought = chain["thought"]
    #         action = chain["action"]
    #         action_input = chain["action_input"]
    #         observation = chain["observation"]
    #         inputs = prompt.replace("{input}", query).replace("{agent_scratchpad}", scratch_pad)
    #         target = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}\n"
    #         scratch_pad += (target + f"Observation: {observation}\n")
    #         tmp_dict = {
    #             "id": f"STEP {step_cnt}: " + query,
    #             "conversations":[
    #                 {
    #                     "from": "human",
    #                     "value": inputs
    #                 },
    #                 {
    #                     "from": "gpt",
    #                     "value": target
    #                 }
    #             ]
    #         }
    #         out_list.append(tmp_dict)
    #     inputs = prompt.replace("{input}", query).replace("{agent_scratchpad}", scratch_pad)
    #     answer = data_dict["answer"]
    #     target = f"Thought: I have got enough information\nFinal Answer:{answer}\n"
    #     tmp_dict = {
    #         "id": f"STEP {step_cnt}: " + query,
    #         "conversations":[
    #             {
    #                 "from": "human",
    #                 "value": inputs
    #             },
    #             {
    #                 "from": "gpt",
    #                 "value": target
    #             }
    #         ]
    #     }
    #     out_list.append(tmp_dict)
    # json.dump(out_list, open(args.output_path,"w"), indent=4, ensure_ascii=False)

def preprocess_multi(tool_data_path):
    # Pick the rev_tools of one given scenario

    '''
    Scenario: vacation plan
    1. google_places
    2. Wikipedia
    3. Weather
    4. Bing_search
    '''
    # rev_tools = '\n\n\n\nCommands(command name: description):\n1. google_places: A tool that query the Google Places API. Useful for when you need to validate or discover addressed from ambiguous text. Input should be a search query.\n2. Wikipedia: A tool to search entity, view content and disambiguate entity on Wikipedia.\nCurrent endpoint for each function is simple and you should only use exact entity name as input for search and disambiguate. And the keyword input to lookup api should also be simple like one or two words.\nSome Tips to use the APIs bertter:\n1) When the search api doesn\'t find the corresponding page, you should search a related entity in the return list.\n2) You can only search one entity name in each action, so, don\'t concat multiple entity names in one search input.\n3) The lookup api can only be used after search api since it depends on the result page of search.\n4) When search api result in an entity page that is not related, you should disambiguate the searched entity to find other entities with the same name.\n5) Don\'t over rely one this simple tool, you may figure out the next action based on your own knowledge.\n3. Weather: Plugin for look up weather information for the given city\n4. Bing_search: Perform Search on Bing Search engine.\nUse search_top3(key: str) to get top 3 search results after input the key to search.\nUse load_page_index(idx: int) to load the detailed page of the search result.\n5. finish: use this to signal that you have finished all your objectives, args: "response": "final response to let people know you have finished your objectives"'

    '''
    Scenario: film topic
    1. Wolfram
    2. Film Search
    3. Slides Making
    4. Wikipedia
    5. file_operation
    6. Bing_search
    '''
    # rev_tools = '\n\n\n\nCommands(command name: description):\n1. Wolfram: Dynamic computation and curated data from WolframAlpha and Wolfram Cloud.\n2. Film Search: Plugin for search for only up-to-date film information.\n3. Slides Making: This tool allows you to create ppt slides with text, paragraph, images, with good looking styles\n4. Wikipedia: A tool to search entity, view content and disambiguate entity on Wikipedia.\nSome Tips to use the APIs bertter:\n1) When the search api doesn\'t find the corresponding page, you should search a related entity in the return list.\n2) You can only search one entity name in each action, so, don\'t concat multiple entity names in one search input.\n3) The lookup api can only be used after search api since it depends on the result page of search.\n4) When search api result in an entity page that is not related, you should disambiguate the searched entity to find other entities with the same name.\n5) Don\'t over rely one this simple tool, you may figure out the next action based on your own knowledge.\nCurrent endpoint for each function is simple and you should only use exact entity name as input for search and disambiguate. And the keyword input to lookup api should also be simple like one or two words.\n5. file_operation: Plugin for operating files\n6. Bing_search: Perform Search on Bing Search engine.\nUse search_top3(key: str) to get top 3 search results after input the key to search.\nUse load_page_index(idx: int) to load the detailed page of the search result.\n7. finish: use this to signal that you have finished all your objectives, args: "response": "final response to let people know you have finished your objectives"'

    '''
    Scenario: file processing
    1. Chemical Property
    2. Meta Analysis
    3. Slides Making
    4. Wikipedia
    5. file_operation
    6. Bing_search
    '''

    rev1 = 'System: You are Jerry, Assistant\nYour decisions must always be made independently \n            without seeking user assistance. Play to your strengths \n            as an LLM and pursue simple strategies with no legal complications. \n            Once you have completed your goal or have found that it can not be finished with current commands, \n            make sure to use the "finish" command immediately.\n\nGOALS:\n\n'
    rev_tools = '\n\n\n\nCommands(command name: description):\n1. Chemical Property: Plugin for looking up a chemical\'s property using a chemical knowledge base. All input should be a json like {{\"input\": "some input"}}. Please use the provided questions and search step by step.\n2. Meta Analysis: Plugin for analyzing literatures. You can draw recording tables and summaries of the given documents to explore the academic topic that you are interested in. You can also search for literatures online. \n3. Slides Making: This tool allows you to create ppt slides with text, paragraph, images, with good looking styles\n4. Wikipedia: A tool to search entity, view content and disambiguate entity on Wikipedia.\nCurrent endpoint for each function is simple and you should only use exact entity name as input for search and disambiguate. And the keyword input to lookup api should also be simple like one or two words.\nSome Tips to use the APIs bertter:\n1) When the search api doesn\'t find the corresponding page, you should search a related entity in the return list.\n2) You can only search one entity name in each action, so, don"t concat multiple entity names in one search input.\n3) The lookup api can only be used after search api since it depends on the result page of search.\n4) When search api result in an entity page that is not related, you should disambiguate the searched entity to find other entities with the same name.\n5) Don"t over rely one this simple tool, you may figure out the next action based on your own knowledge.\n5. file_operation: Plugin for operating files\n6. Bing_search: Perform Search on Bing Search engine.\nUse search_top3(key: str) to get top 3 search results after input the key to search.\nUse load_page_index(idx: int) to load the detailed page of the search result.\n7. finish: use this to signal that you have finished all your objectives, args: "response": "final response to let people know you have finished your objectives\"'
    rev2 = rev_tools + '\n\nPerformance Evaluation:\n1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.\n2. Constructively self-criticize your big-picture behavior constantly.\n3. Reflect on past decisions and strategies to refine your approach.\n4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps. Remember what you have done! Do not use same commands repeatedly even if no results returned.\n\nYou should only respond in JSON format WITHOUT any other content or markers, and the command name has to be one of the names above. The format is described below \nResponse Format: \n{\n    "thoughts": {\n        "text": "thought",\n        "reasoning": "reasoning"\n    },\n    "command": {\n        "name": "command name",\n        "args": {\n            "goal": "the detailed description and necessary information of the subtask that you hope current command can achieve"\n        }\n    }\n} \nEnsure the response can be parsed by Python json.loads\nSystem: The current time and date is Wed May 17 13:25:30 2023\nSystem: This reminds you of these commands you have already used, and NEVER conduct repeated or unrelated commands:\nHuman: Determine which next command to use, and respond using the format specified above:\n'

    # Add tool prompt

    ### Wolfram
    tool_Wolfram = 'Answer the following questions as best you can. General instructions are: Dynamic computation and curated data from WolframAlpha and Wolfram Cloud.. Specifically, you have access to the following APIs:\n\ngetWolframAlphaResults: Get Wolfram|Alpha results using natural query. Queries to getWolframAlphaResults must ALWAYS have this structure: {{"input": query}}. And please directly read the output json.. Your input should be a json (args json schema): {{"input" : string, }} The Action to trigger this API should be getWolframAlphaResults and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [getWolframAlphaResults]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### chemical property
    tool_Chemical_Property = 'Answer the following questions as best you can. General instructions are: Plugin for looking up a chemical\'s property using a chemical knowledge base. All input should be a json like {\'input\': \'some input\'}. Please use the provided questions and search step by step.. Specifically, you have access to the following APIs:\n\nget_name: prints the possible 3 synonyms of the queried compound ID. Your input should be a json (args json schema): {"cid" : string, } The Action to trigger this API should be get_name and the input parameters should be a json dict string. Pay attention to the type of parameters.\nget_allname: prints all the possible synonyms (might be too many, use this function carefully).. Your input should be a json (args json schema): {"cid" : string, } The Action to trigger this API should be get_allname and the input parameters should be a json dict string. Pay attention to the type of parameters.\nget_id_by_struct: prints the ID of the queried compound SMILES. This should only be used if smiles is provided or retrieved in the previous step. The input should not be a string, but a SMILES formula.. Your input should be a json (args json schema): {"smiles" : string, } The Action to trigger this API should be get_id_by_struct and the input parameters should be a json dict string. Pay attention to the type of parameters.\nget_id: prints the ID of the queried compound name, and prints the possible 5 names if the queried name can not been precisely matched,. Your input should be a json (args json schema): {"name" : string, } The Action to trigger this API should be get_id and the input parameters should be a json dict string. Pay attention to the type of parameters.\nget_prop: prints the properties of the queried compound ID. Your input should be a json (args json schema): {"cid" : string, } The Action to trigger this API should be get_prop and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [get_name, get_allname, get_id_by_struct, get_id, get_prop]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### google places
    tool_google_places = 'Answer the following questions as best you can. General instructions are: A tool that query the Google Places API. Useful for when you need to validate or discover addressed from ambiguous text. Input should be a search query.. Specifically, you have access to the following APIs:\n\nsearch_places: Run Places search.. Your input should be a json (args json schema): {{"query" : string, }} The Action to trigger this API should be search_places and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [search_places]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### douban
    tool_Film_Search = 'Answer the following questions as best you can. General instructions are: Plugin for search for only up-to-date film information.. Specifically, you have access to the following APIs:\n\ncoming_out_filter: coming_out_filter(args: str) prints the details of the filtered [outNum] coming films now according to region, cate and outNum. \nargs is a list like "str1, str2, str3, str4"\nstr1 represents Production country or region. If you cannot find a region, str1 is 全部\nstr2 represents movie"s category. If you cannot find a category, str2 is 全部\nstr3 can be a integer number that agent want to get. If you cannot find a number, str2 is 100. If the found movie"s num is less than str2, Final Answer only print [the found movie"s num] movies.\nstr4 can be a True or False that refluct whether agent want the result sorted by people number which look forward to the movie.\nFinal answer should be complete.\n\nThis is an example:\nThought: I need to find the upcoming Chinese drama movies and the top 2 most wanted movies\nAction: coming_out_filter\nAction Input: {{"args" : "中国, 剧情, 2, True"}}\nObservation: {{"date":{{"23":"04月28日","50":"07月"}},"title":{{"23":"长空之王","50":"热烈"}},"cate":{{"23":"剧情 / 动作","50":"剧情 / 喜剧"}},"region":{{"23":"中国大陆","50":"中国大陆"}},"wantWatchPeopleNum":{{"23":"39303人","50":"26831人"}}}}\nThought: I now know the top 2 upcoming Chinese drama movies\nFinal Answer: 即将上映的中国剧情电影有2部：长空之王、热烈，大家最想看的前2部分别是：长空之王、热烈。. Your input should be a json (args json schema): {{"args" : string, }} The Action to trigger this API should be coming_out_filter and the input parameters should be a json dict string. Pay attention to the type of parameters.\nnow_playing_out_filter: NowPlayingOutFilter(args: str) prints the details of the filtered [outNum] playing films now according to region, scoreSort\nargs is a list like "str1, str2, str3"\nstr1 can be "中国","日本" or other Production country or region. If you cannot find a region, str1 is 全部\nstr2 can be a integer number that agent want to get. If you cannot find a number, str2 is 100. If the found movie"s num is less than str2, Final Answer only print [the found movie"s num] movies.\nstr3 can be a True or False that refluct whether agent want the result sorted by score.\nFinal answer should be complete.\n\nThis is an example:\nInput: 您知道现在有正在上映中国的电影吗？请输出3部\nThought: I need to find the currently playing movies with the highest scores\nAction: now_playing_out_filter\nAction Input: {{"args" : "全部, 3, True"}}\nObservation: {{"title":{{"34":"切腹","53":"吉赛尔","31":"小森林 夏秋篇"}},"score":{{"34":"9.4","53":"9.2","31":"9.0"}},"region":{{"34":"日本","53":"西德","31":"日本"}},"director":{{"34":"小林正树","53":"Hugo Niebeling","31":"森淳一"}},"actors":{{"34":"仲代达矢 / 石浜朗 / 岩下志麻","53":"卡拉·弗拉奇 / 埃里克·布鲁恩 / Bruce Marks","31":"桥本爱 / 三浦贵大 / 松冈茉优"}}}}\nThought: I now know the currently playing movies with the highest scores\nFinal Answer: 现在上映的评分最高的3部电影是：切腹、吉赛尔、小森林 夏秋篇. Your input should be a json (args json schema): {{"args" : string, }} The Action to trigger this API should be now_playing_out_filter and the input parameters should be a json dict string. Pay attention to the type of parameters.\nprint_detail: parsing_detail_page(args) prints the details of an up-to-date movie you have already filtered out, giving its name.\n            args is a list like "str1"\n            str1 is target movie"s name.\n            step1: apply function parse_coming_page and parse_nowplaying_page and get all movie"s links and other infomation.\n            step2: get the target movie"s link from df_coming or df_nowplaying\n            step3: get detail from step2"s link\n\n            This is an example: \n            Input: "电影流浪地球2怎么样？"\n            Thought: I need to find the movie"s information\n            Action: print_detail\n            Action Input: {{"args" : "流浪地球2"}}\n            Observation: "是一部中国大陆的科幻、冒险、灾难电影，由郭帆导演，吴京、刘德华、李雪健等人主演.\n剧情简介：太阳即将毁灭，人类在地球表面建造出巨大的推进器，寻找新的家园。然而宇宙之路危机四伏，为了拯救地球，流浪地球时代的年轻人再次挺身而出，展开争分夺秒的生死之战。"\n            Thought: I now know the final answer\n            Final Answer: 流浪地球2是一部中国大陆的科幻、冒险、灾难电影，由郭帆导演，吴京、刘德华、李雪健等人主演，剧情简介是太阳即将毁灭，人类在地球表面建造出巨大的推进器，寻找新的家园，然而宇宙之路危机四伏，为了拯救地球，流浪地球时代的年轻人再次挺身而出，. Your input should be a json (args json schema): {{"args" : string, }} The Action to trigger this API should be print_detail and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [coming_out_filter, now_playing_out_filter, print_detail]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### Meta Analysis
    tool_Meta_Analysis = 'Answer the following questions as best you can. General instructions are: Plugin for analyzing literatures. You can draw recording tables and summaries of the given documents to explore the academic topic that you are interested in. You can also search for literatures online.. Specifically, you have access to the following APIs:\n\nsearch_literature: Search for the given topic literatures in the database if the literature file is not provided. This will return the path of a pickle file recording literatures, and the number of literatures. The searching term should be key words in the topic (2-5 words). the number of literatures will be less than maxnum (recommend 15). Such as:\nAction: search_literature\nAction Input: {"topic":"Side effects of ibuprofen for menstrual period pain relief", "maxnum":15, "term":"ibuprofen menstrual side effect"}. Your input should be a json (args json schema): {"topic" : string, "maxnum" : integer, "term" : string, } The Action to trigger this API should be search_literature and the input parameters should be a json dict string. Pay attention to the type of parameters.\nsplit_criteria: Split the screening requirements in the criteria of the literatures into a series of simple yes/no problems, and return the path of the splitted questions. Such as:\nAction: split_criteria\nAction Input: {"criteria":"literatures comparing ibuprofen and other pain treatments or placebo, and reporting side effects for menstrual period females"}. Your input should be a json (args json schema): {"criteria" : string, } The Action to trigger this API should be split_criteria and the input parameters should be a json dict string. Pay attention to the type of parameters.\nliterature_filter: Check each literatures saved in the literature path according to the questions saved in the question path, and return the literatures that match the requirements. Concat path is the concatenated string of literature path and question path connected with \'&&&\'. Such as:\nAction: literature_filter\nAction Input: {"concat_path": "myarticles.pkl&&&split_ques_new.pkl"}. Your input should be a json (args json schema): {"concat_path" : string, } The Action to trigger this API should be literature_filter and the input parameters should be a json dict string. Pay attention to the type of parameters.\ndraw_table: Extract the important elements of the literatures recorded in the given pickle file and return the path of table records. concatenate the literature path and the analysis topic with \'&&&\' as the input. Such as:\nAction: draw_table\nAction Input: {"literature_path_and_topic":"myfile.pkl&&&ibuprofen side effect"}. Your input should be a json (args json schema): {"literature_path_and_topic" : string, } The Action to trigger this API should be draw_table and the input parameters should be a json dict string. Pay attention to the type of parameters.\ncombine_table: Combine several tables recorded in the table path into one comprehensive record table and return. give the literature path, table path and the exploring topic as the input. Such as:\nAction: combine_table\nAction Input: {"literature_path":"myfile.pkl", "table_path":"mytable.txt", "topic":"ibuprofen side effect"}. Your input should be a json (args json schema): {"literature_path" : string, "table_path" : string, "topic" : string, } The Action to trigger this API should be combine_table and the input parameters should be a json dict string. Pay attention to the type of parameters.\ngenerate_summary: Given the exploring topic and the record table path of the literatures, this tool generates a paragraph of summary. Such as:\nAction: generate_summary\nAction Input: {"topic": "ibuprofen side effect", "table_path":"mytable.txt"}. Your input should be a json (args json schema): {"topic" : string, "table_path" : string, } The Action to trigger this API should be generate_summary and the input parameters should be a json dict string. Pay attention to the type of parameters.\nprint_literature: given the literature path and number that are required to display, this tool returns the title and abstract of the literature.. Your input should be a json (args json schema): {"literature_path" : string, "print_num" : integer, } The Action to trigger this API should be print_literature and the input parameters should be a json dict string. Pay attention to the type of parameters.\nprint_tablefile: given the table file path that are required to display, this tool reads the file and returns the string of the table.. Your input should be a json (args json schema): {"table_path" : string, } The Action to trigger this API should be print_tablefile and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [search_literature, split_criteria, literature_filter, draw_table, combine_table, generate_summary, print_literature, print_tablefile]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### ppt
    tool_Slides_Making = 'Answer the following questions as best you can. General instructions are: This tool allows you to create ppt slides with text, paragraph, images, with good looking styles. Specifically, you have access to the following APIs:\n\ncreate_file: create_file(theme:str) -> None: Create a pptx file with specific theme, available thems: green / orange / tech / wooden / flat.. Your input should be a json (args json schema): {{"theme" : string, }} The Action to trigger this API should be create_file and the input parameters should be a json dict string. Pay attention to the type of parameters.\nget_image: get_image(keywords:str) -> str Get an image given comma seperated keywords, return the image path.. Your input should be a json (args json schema): {{"keywords" : string, }} The Action to trigger this API should be get_image and the input parameters should be a json dict string. Pay attention to the type of parameters.\nadd_first_page: add_first_page(title:str, subtitle:str) -> None: Add the first page of ppt.. Your input should be a json (args json schema): {{"title" : string, "subtitle" : string, }} The Action to trigger this API should be add_first_page and the input parameters should be a json dict string. Pay attention to the type of parameters.\nadd_text_page: add_text_page(title:str, bullet_items:str) -> None: Add text page (outline page is also applied).\nbullet_items should be string, for multiple bullet items, please use [SPAN] to separate them.. Your input should be a json (args json schema): {{"title" : string, "bullet_items" : string, }} The Action to trigger this API should be add_text_page and the input parameters should be a json dict string. Pay attention to the type of parameters.\nadd_text_image_page: add_text_image_page(title:str, bullet_items:str, image:str) -> None: Add a text page with one image. (image should be a path)\nbullet_items should be string, for multiple bullet items, please use [SPAN] to separate them.. Your input should be a json (args json schema): {{"title" : string, "bullet_items" : string, "image" : string, }} The Action to trigger this API should be add_text_image_page and the input parameters should be a json dict string. Pay attention to the type of parameters.\nsubmit_file: submit_file(name:str) -> None: When all steps done, YOU MUST use submit_file() to submit your work in your topic name.. Your input should be a json (args json schema): {{"name" : string, }} The Action to trigger this API should be submit_file and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [create_file, get_image, add_first_page, add_text_page, add_text_image_page, submit_file]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use\nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### Weather
    tool_Weather = 'Answer the following questions as best you can. General instructions are: Plugin for look up weather information for the given city. Specifically, you have access to the following APIs:\n\nget_weather_today: gets the weather today for the specific given location, such as:\nAction: get_weather_today\nAction Input: {{"location": "Beijing"}}. Your input should be a json (args json schema): {{"location" : string, }} The Action to trigger this API should be get_weather_today and the input parameters should be a json dict string. Pay attention to the type of parameters.\nforecast_weather: Forecast weather in the upcoming number of days for the specific given location, such as:\nAction: forecast_weather\nAction Input: {{"location": "Beijing", "days": "3"}}. Your input should be a json (args json schema): {{"location" : string, "days" : string, }} The Action to trigger this API should be forecast_weather and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [get_weather_today, forecast_weather]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### Wikipedia
    tool_Wikipedia = 'Answer the following questions as best you can. General instructions are: A tool to search entity, view content and disambiguate entity on Wikipedia.\nCurrent endpoint for each function is simple and you should only use exact entity name as input for search and disambiguate. And the keyword input to lookup api should also be simple like one or two words.\nSome Tips to use the APIs better:\n1) When the search api doesn\'t find the corresponding page, you should search a related entity in the return list.\n2) You can only search one entity name in each action, so, don\'t concat multiple entity names in one search input.\n3) The lookup api can only be used after search api since it depends on the result page of search.\n4) When search api result in an entity page that is not related, you should disambiguate the searched entity to find other entities with the same name.\n5) Don\'t over rely one this simple tool, you may figure out the next action based on your own knowledge.. Specifically, you have access to the following APIs:\n\nsearch: The input is an exact entity name. The action will search this entity name on Wikipedia and returns the first five sentences if it exists. If not, it will return some related entities to search next.. Your input should be a json (args json schema): {"entity" : string, } The Action to trigger this API should be search and the input parameters should be a json dict string. Pay attention to the type of parameters.\nlookup: The input is a concise keyword. This action will look up in the current passage and return the next several sentences containing the keyword in current passage.. Your input should be a json (args json schema): {"keyword" : string, } The Action to trigger this API should be lookup and the input parameters should be a json dict string. Pay attention to the type of parameters.\ndisambiguation: The input is an entity name. This action will disambiguate this entity name to find other entities with similar names in Wikipedia.. Your input should be a json (args json schema): {"entity" : string, } The Action to trigger this API should be disambiguation and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [search, lookup, disambiguation]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### file operation
    tool_file_operation = 'Answer the following questions as best you can. General instructions are: Plugin for operating files. Specifically, you have access to the following APIs:\n\nwrite_file: write file to disk. Your input should be a json (args json schema): {{"file_path" : string, "text" : string, }} The Action to trigger this API should be write_file and the input parameters should be a json dict string. Pay attention to the type of parameters.\nread_file: read file from disk and return the content. Your input should be a json (args json schema): {{"file_path" : string, }} The Action to trigger this API should be read_file and the input parameters should be a json dict string. Pay attention to the type of parameters.\nconvert_pickle: Combine the file in txt directory into a dict and save in pickle file, which can be further processed and analyzed. Such as:\nAction: convert_pickle\nAction Input: {{"txt_dir":"./textdata/origin", "pickle_path":"./origin_converted.pkl"}}. Your input should be a json (args json schema): {{"txt_dir" : string, "pickle_path" : string, }} The Action to trigger this API should be convert_pickle and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [write_file, read_file, convert_pickle]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    ### bing
    tool_Bing_search = 'Answer the following questions as best you can. General instructions are: Perform Search on Bing Search engine.\nUse search_top3(key: str) to get top 3 search results after input the key to search.\nUse load_page_index(idx: int) to load the detailed page of the search result.. Specifically, you have access to the following APIs:\n\nsearch_top3: Search key words, return top 3 search results. Such as:\nAction: search_top3\nAction Input: {{"key_words": "University in Beijing"}}. Your input should be a json (args json schema):{{"key_words" : string, }} The Action to trigger this API should be search_top3 and the input parameters should be a json dict string. Pay attention to the type of parameters.\nload_page_index: Load page detail of the search result indexed as "idx", and return the content of the page. Such as:\nAction: load_page_index\nAction Input: {{"idx":0}}. Your input should be a json (args json schema): {{"idx" : string, }} The Action to trigger this API should be load_page_index and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [search_top3, load_page_index]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\n. The action you generate must be exact one of the given API names instead of a sentence or any other redundant text. The action input is one json format dict without any redundant text or bracket descriptions . (2) Provide as much as useful information (such as useful values/file paths in your observation) in your Final Answer. Do not describe the process you achieve the goal, but only provide the detailed answer or response to the task goal. (3) Do not make up anything. (4) Read the observation carefully, and pay attention to the messages even if an error occurs. (5) Once you have enough information, please immediately use \nThought: I have got enough information\nFinal Answer: \n\nTask: {input}\n{agent_scratchpad}'

    out_list = []
    def process(tool_data_path):
        data_dicts = json.load(open(tool_data_path, "r"))
        for line in data_dicts:
            scratch_pad = ""
            tmp_list = []
            goal = line['query'].replace('\n','')
            prompt = rev1 + goal.replace('\n','') + rev2
            steps = line['steps']
            tool_obervs = []

            for step in steps:
                ans_out = step['assistant_reply'].replace('\n','')
                try:
                    ans_out_json = json.loads(ans_out)
                    tool_name = ans_out_json['command']['name']
                    goal_tool= ans_out_json['command']['args']['goal']
                except:
                    continue
                
                tmp_list.append([prompt, ans_out])
                prompt += ans_out 
                prompt += '\n'

                # Add tool prompt 
                if tool_name == "Chemical Property":
                    inner_prompt = tool_Chemical_Property
                elif tool_name == "Meta Analysis":
                    inner_prompt = tool_Meta_Analysis
                elif tool_name == "Slides Making":
                    inner_prompt = tool_Slides_Making
                elif tool_name == "Wikipedia":
                    inner_prompt = tool_Wikipedia
                elif tool_name == "file_operation":
                    inner_prompt = tool_file_operation
                elif tool_name == "Bing_search":
                    inner_prompt = tool_Bing_search
                elif tool_name == "Weather":
                    inner_prompt = tool_Weather
                elif tool_name == "Film Search":
                    inner_prompt = tool_Film_Search
                elif tool_name == "Wolfram":
                    inner_prompt = tool_Wolfram
                elif tool_name == "google_places":
                    inner_prompt = tool_google_places
                else:
                    continue

                inner_prompt = inner_prompt.replace("{input}\n{agent_scratchpad}", '{\"goal\": '+goal_tool+'\"' + ',' + '"history context": "['+','.join(tool_obervs)[-500:]+']"}\n')

                length_log = 0
                for tool_log in step['chains']:
                    if length_log == (len(step['chains'])-1):
                        tmp_list.append([inner_prompt, tool_log["observation"]])
                        prompt += ("\nSystem: "+step['answer'])
                        prompt += "\nHuman: Determine which next command to use, and respond using the format specified above:"
                        tool_obervs.append(step['answer'])
                        break
                    thought = tool_log["thought"]
                    action = tool_log["action"]
                    action_input = tool_log["action_input"]
                    chain = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}"
                    tmp_list.append([inner_prompt, chain])
                    inner_prompt += chain
                    inner_prompt += ('\nObservation:'+tool_log["observation"])
                    inner_prompt += '\nThought:'
                    scratch_pad += (tool_log["observation"] + f"Observation: {chain}\n")
                    length_log += 1

            for step_cnt, inp_out_pair in enumerate(tmp_list):
                inp, out = inp_out_pair
                tmp_dict = {
                    "id": f"STEP {step_cnt}: " + goal,
                    "conversations":[
                        {
                            "from": "human",
                            "value": inp
                        },
                        {
                            "from": "gpt",
                            "value": out
                        }
                    ]
                }
                out_list.append(tmp_dict)

    process(tool_data_path)
    json.dump(out_list, open(args.output_path,"w"), indent=4, ensure_ascii=False)
        

if __name__=='__main__':
    if args.tool_mode == "single":
        preprocess_single(args.tool_data_path)
    elif args.tool_mode == "multi":
        preprocess_multi(args.tool_data_path)
    else:
        print(f"Unrecognized tool mode {args.tool_mode}. Should be 'single' or 'multi'")