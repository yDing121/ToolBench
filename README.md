<div align= "center">
    <h1> 🛠️ToolBench🤖</h1>
</div>

<div align="center">

![Dialogues](https://img.shields.io/badge/Tool\_Num-29-red?style=flat-square)
![Dialogues](https://img.shields.io/badge/API\_Num-86-red?style=flat-square)
![Dialogues](https://img.shields.io/badge/Current\_Dataset\_Size-98K-red?style=flat-square)
![Dialogues](https://img.shields.io/badge/Total\_API\_Call-312K-red?style=flat-square)
![Dialogues](https://img.shields.io/badge/Tool\_LLaMA-Released-green?style=flat-square)

</div>

<p align="center">
  <a href="#model">Model</a> •
  <a href="#data">Data Release</a> •
  <a href="https://github.com/OpenBMB/BMTools">Toolkit</a> •
  <a href="https://arxiv.org/abs/2304.08354">Paper</a> •
  <a href="https://github.com/thunlp/ToolLearningPapers">Paper List</a> •
  <a href="#citation">Citation</a> •

</p>

</div>


🔨This project aims to construct **open-source, large-scale, high-quality** instruction tuning SFT data to facilitate the construction of powerful LLMs with general **tool-use** capability. We provide the dataset, the corresponding training and evaluation scripts, and a capable model ToolLLaMA fine-tuned on ToolBench.

✨More details and our paper about ToolBench and ToolLLaMA are coming soon!

<div align="center">
<img src="https://cdn.discordapp.com/attachments/941582479117127680/1111543600879259749/20230526075532.png" width="400px">
</div>

✨✨Features:
 - Both **single-tool** and **multi-tool** scenarios are supported in ToolBench. The single-tool setting follows [LangChain](https://github.com/hwchase17/langchain) style (prompt), and the multi-tool setting follows the [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT) style (prompt).
 - ToolBench provides responses that not only include the final answer but also incorporate the model's **chain-of-thought process, tool execution, and tool execution results**. 
 - ToolBench embraces the complexity of real-world scenarios, enabling **multi-step** tool invocations.
 - Another notable advantage is the **diversity** of our API, which is designed for **real-world scenarios** such as weather information, search functionality, stock updates, and PowerPoint automation. 
 - All the data is automatically generated by OpenAI API and filtered by us, the whole data creation process is easy to scale up.

<br>
<div align="center">
<img src="https://cdn.discordapp.com/attachments/941582479117127680/1111210433307750451/ToolLLaMA.png" width="800px">
</div>
<br>

*Please note that current released data is still not the final version. We are conducting extensive post-processing to improve the data quality and increase the coverage of real-world tools.*

<!-- 💁‍♂️💁💁‍♀️**We need your help!** Curating large-scale real-world APIs and their corresponding tool-use SFT data is not easy, we sincerely invite you to join us in building and refining ToolBench. We will list all participants as co-authors in the final paper. Please contact and join [us](mailto:yujiaqin16@gmail.com) if you're interested. -->

## 🗒️Data

👐ToolBench is intended solely for research and educational purposes and should not be construed as reflecting the opinions or views of the creators, owners, or contributors of this dataset. It is distributed under [CC BY NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/).

ToolBench contains both single-tool and multi-tool scenarios, below is the statistics for the single-tool scenario:

| Tool           | Query Num | Chains Num | Chains/Query |
|----------------|-----------|------------|------------------|
| Weather        | 9827      | 23740      | 2.4              |
| Chemical       | 8585      | 29916      | 3.5              |
| Translation    | 10267     | 23011      | 2.2              |
| Map            | 7305      | 23325      | 3.2              |
| Stock          | 11805     | 32550      | 2.8              |
| Meta analysis  | 2526      | 15725      | 6.2              |
| Bing search    | 31089     | 102088     | 3.3              |
| Wolfram        | 16130     | 56169      | 3.5              |
| Database       | 1264      | 6347       | 5                |

Statistics for multi-tool scenario:

| Scenario      | Tools                                                                          | Query num | Sub-Query num | Chains num | Chains per Query |
|---------------|--------------------------------------------------------------------------------|-----------|---------------|------------|------------------|
| Meta_file     | chemical-prop/meta_analysis/Slides Making/Wikipedia/file_operation/Bing_search | 331       | 1197          | 5899       | 17.8             |
| Multi_film    | Wolfram/Film Search/Slides Making/Wikipedia/file_operation/Bing_search         | 795       | 2703          | 12445      | 15.7             |
| Vacation_plan | google_places/wikipedia/weather/bing search                                    | 191       | 654           | 2742       | 14.4             |

### Data Release

For single tool data we release 1000 instances for each tool, and for multi tool data we release all the data. Please download our dataset using the following link: [Data](https://drive.google.com/drive/folders/1OaB-hM7eRiWi3TeqHij24VT9MAqgvC0H?usp=drive_link).

### Data Format
Each line in the downloaded data file is a json dict containing the prompt templated for data creation, human instruction (query) for tool use, intermediate thoughts / tool executions loops, and the final answer. Below we show an example for single tool data generation.

```
Tool Descrition:
BMTools Tool_name: translation
Tool action: get_translation
action_input: {"text": target texts, "tgt_lang": target language}

Generated Data:
{
    "prompt": "Answer the following questions as best you can. Specifically, you have access to the following APIs:\n\nget_translation: . Your input should be a json (args json schema): {{\"text\" : string, \"tgt_lang\" : string, }} The Action to trigger this API should be get_translation and the input parameters should be a json dict string. Pay attention to the type of parameters.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [get_translation]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times, max 7 times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\nFinal Answer:\n (2) Provide as much as useful information in your Final Answer. (3) Do not make up anything, and if your Observation has no link, DO NOT hallucihate one. (4) If you have enough information and want to stop the process, please use \nThought: I have got enough information\nFinal Answer: **your response. \n The Action: MUST be one of the following:get_translation\nQuestion: {input}\n Agent scratchpad (history actions):\n {agent_scratchpad}",
    "query": "My intention is to convert the data provided in ما هي الأقسام الثلاثة للقوات المسلحة؟ into Arabic(ara).\n",
    "chains": [
        {
            "thought": "I need to use the get_translation API to convert the text into Arabic.",
            "action": "get_translation",
            "action_input": "{\"text\": \"What are the three branches of the military?\", \"tgt_lang\": \"ara\"}",
            "observation": "\"ما هي الفروع الثلاثة للجيش ؟\""
        }
    ],
    "answer": "The translation of \"What are the three branches of the military?\" into Arabic is \"ما هي الفروع الثلاثة للجيش ؟\"."
}

```

Multi-tool example:

```
Here is an example of using Bing_Search tool, and PPT tool in BMTools:

{
        "query": "Can you find me examples of successful renewable energy projects in Africa? Please compile a list of case studies with details on the technologies used, costs, and environmental impact.\n",
        "steps": [
            {
                "assistant_reply": "{\n    \"thoughts\": {\n        \"text\": \"I think I should use the Bing_search command to look for successful renewable energy projects in Africa.\",\n        \"reasoning\": \"As an Assistant with legal background, I do not have enough knowledge to list out these projects. Therefore, I think it's a good idea to research and find some project examples on the internet. Bing_search is a suitable command for me since I can use it to perform searches on the internet.\"\n    },\n    \"command\": {\n        \"name\": \"Bing_search\",\n        \"args\": {\n            \"goal\": \"Find successful renewable energy projects in Africa\"\n        }\n    }\n}",
                "chains": [
                    {
                        "thought": "I need to search for examples of successful renewable energy projects in Africa.",
                        "action": "search_top3",
                        "action_input": "{\"key_words\": \"successful renewable energy projects Africa\"}",
                        "observation": "\"page: 1\\ntitle: This is the state of renewable energy in Africa right now\\nsummary: Africa. In 2020, 9% of all energy generated in Africa came from renewable sources, reports Statista. North Africa is the current leader on the continent in terms of renewable energy capacity. While Southern Africa is lagging behind, with just over 4,000 MW capacity.\\npage: 2\\ntitle: Lighting Up Africa: Bringing Renewable, Off-Grid Energy to Communities\\nsummary: Lighting Up Africa: Bringing Renewable, Off-Grid Energy to Communities. Photo credit: John Deyegbe/Resolution Ltd. This story is the first in a series to showcase the tools, approaches, evidence, and results of more than 300 projects in pursuit of climate-smart development under the Africa Climate Business Plan.\\npage: 3\\ntitle: The Renewable Energy Transition in Africa\\nsummary: Promote access to energy; De-risk and promoting private sector investments; Strengthen and modernise the grid; Support systemic innovation. The study also explores the transformational potential of the electricity sector in five Africa countries: Ghana, Ivory Coast, Morocco, Rwanda and South Africa.\\n\""
                    },
                    .....
                ],
                "answer": "Tool Bing_search returned: {'input': '{\"goal\": \"Find successful renewable energy projects in Africa\", \"history context\": \"[]\"}', 'output': 'The top 3 search results for \"successful renewable energy projects Africa\" do not provide specific information about successful renewable energy projects in Africa, but rather provide general information about the state of renewable energy in Africa and initiatives to promote it.'}"
            },
            .....
            {
                "assistant_reply": "{\n    \"thoughts\": {\n        \"text\": \"I think I should use the Slides Making command to create a presentation on renewable energy projects in Africa based on the information that we have collected so far.\",\n        \"reasoning\": \"Since I have not been able to find any specific information on successful renewable energy projects in Africa, I believe that creating a presentation using the information that we have collected so far might be a good idea. Slides Making is a suitable command for creating professional-looking presentations with text, paragraphs, and images, thereby allowing us to summarize and present the information that we have found in an effective manner.\"\n    },\n    \"command\": {\n        \"name\": \"Slides Making\",\n        \"args\": {\n            \"goal\": \"Create a presentation on renewable energy projects in Africa\"\n        }\n    }\n}",
                "chains": [
                    {
                        "thought": "We need to create a pptx file with a specific theme first before adding content to it.",
                        "action": "create_file",
                        "action_input": "{\"theme\":\"green\"}",
                        "observation": "\"created a ppt file.\""
                    },
                    ...
                ],
                "answer": "Tool Slides Making returned: {'input': '{\"goal\": \"Create a presentation on renewable energy projects in Africa\", \"history context\": \"[\\\\\"Tool Bing_search returned: {\\\\\\\\\\\\\"input\\\\\\\\\\\\\": \\\\\\\\\\\\\"{\"goal\": \"Find successful renewable energy projects in Africa\", \"history context\": \"[]\"}\\\\\\\\\\\\\", \\\\\\\\\\\\\"output\\\\\\\\\\\\\": \\\\\\\\\\\\\"The top 3 search results for \"successful renewable energy projects Africa\" do not provide specific information about successful renewable energy projects in Africa, but rather provide general information about the state of renewable energy in Africa and initiatives to promote it.\\\\\\\\\\\\\"}\\\\\"]\"}', 'output': 'The final pptx presentation can be found at the file path: /Users/ava/Downloads/BMTools-zzn0513_copy/cache/1684750606.0464199Renewable Energy Projects in Africa.pptx'}"
            }
        ]
    },

```




Here is an example of the data creation process using BMTools:

<div align="center">

<img src="assets/meta0423.gif" width="700px">

</div>

## 🤖Model

We release the 7b lora version of ToolLLaMA, [single-tool model](https://huggingface.co/pooruss-lsh/tool-llama7b-single-tool-lora) and [multi-tool model](https://huggingface.co/pooruss-lsh/tool-llama7b-multi-tool-lora) which are both trained on the released dataset. The models are trained in a multi-task fashion.

## 🚀Fine-tuning
### Install
Clone this repository and navigate to the ToolLLaMA folder.
```bash
git clone git@github.com:OpenBMB/ToolBench.git
cd ToolLLaMA
```
Install Package (python>=3.9)
```bash
pip install -r requirements.txt
```

### Data Preprocess
Download our newly released tool data and put them under `data/original/`. For single tool data preprocessing, you can use the following command to process the data for fine-tuning.:
```bash
python data/preprocess.py \
    --tool_mode single
    --tool_data_path data/original/weather_demo.json \
    --output_path data/processed/weather_demo.json
```
For multi tools data preprocessing, you can use:
```bash
python data/preprocess.py \
    --tool_mode multi
    --tool_data_path data/original/meta_file_demo.json \
    --output_path data/processed/meta_file_demo.json
```

### Train
Our code is based on [FastChat](https://github.com/lm-sys/FastChat). You can use the following command to train ToolLLaMA-7b with 4 x A100 (40GB):
```bash
export PYTHONPATH=./
torchrun --nproc_per_node=4 --master_port=20001 toolbench/train/train_mem.py \
    --model_name_or_path huggyllama/llama-7b  \
    --data_path  data/processed/weather_processed.json \
    --bf16 True \
    --output_dir output \
    --num_train_epochs 3 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "steps" \
    --eval_steps 1500 \
    --save_strategy "steps" \
    --save_steps 1500 \
    --save_total_limit 8 \
    --learning_rate 5e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.04 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True
```

## Inference

### Install BMTools
The tool execution is supported by [BMTools](https://github.com/OpenBMB/BMTools). First clone BMTools under current directory and build up settings:
```bash
git clone git@github.com:OpenBMB/BMTools.git
cd BMTools
pip install --upgrade pip
pip install -r requirements.txt
python setup.py develop
cd ..
```

Then add your api keys to secret_keys.sh, and start the local tools:
```bash
source BMTools/secret_keys.sh
python BMTools/host_local_tools.py
```

### Inference with Command Line Interface
Prepare for the api keys and python path:
```bash
source BMTools/secret_keys.sh
export PYTHONPATH=BMTools
```

The command below requires around 14GB of GPU memory for ToolLLaMA-7B. Replace `/path/to/ToolLLaMA/weights` with your converted ToolLLaMA weights path.
- For single tool inference:
```bash
python toolbench/inference/inference_single_tool.py \
    --tool_name weather \
    --model_path /path/to/ToolLLaMA/weights
```
for lora:
```bash
python toolbench/inference/inference_single_tool.py \
    --tool_name weather \
    --model_path /path/to/llama/weights \
    --lora_path /path/to/lora/weights
```
- For multi tools inference:
```bash
python toolbench/inference/inference_multi_tools.py \
    --model_path /path/to/ToolLLaMA/weights
```


## Evaluation

The general idea of ToolBench is to train a LLM in our supervised data which then will support in [BMTools](https://github.com/OpenBMB/BMTools).
Each sector of ToolBench has its own challenges and requires particular strategy designs. 

### Model Experiment

- Machine Evaluation 

We randomly sample 100 chain steps in each tool to build our machine evaluation testbed. On average, there are 27 final steps and 73 intermediate tool calling steps. We evaluate the final steps with Rouge-L and the intermediate steps with ExactMatch.

| model_name                   | Downsampling | Beam size | Overall - Final Answer | Overall - Action | Overall - Input |
|------------------------------|--------------|-----------|------------------------|------------------|-----------------|
| cpmbee-finetuned             | 0.05         | 1         | **0.55**               | 0.64             | 0.40            |
| llama7b-finetuned            | 0.05         | 1         | 0.27                   | **0.77**         | 0.53            |
| vicuna7b-finetuned           | 0.05         | 1         | 0.42                   | 0.53             | 0.40            |
| llama7b-finetuned            | 0.5          | 1         | 0.35                   | 0.67             | 0.50            |
| llama7b-finetuned            | 0.7          | 1         | 0.29                   | 0.74             | **0.56**        |

- Human Evaluation

We randomly sample 10 query in each of the following tools: Weather, Map, Stock, Translation, Chemical and WolframAlpha. We evaluate the pass rate of tool calling process, final answer, and the final answer comparison with chatgpt.

| model_name                   | Downsampling | Beam size |  Tool Calling Process  |   Final Answer   |   Comparison   |
|------------------------------|--------------|-----------|------------------------|------------------|----------------|
| llama7b-finetuned            | 0.05         | 1         | **90%**                | **76.7%**        | 11.7%/60%/28.3%|


- ChatGPT Evaluation

We perform an automatic evluation by ChatGPT which scoring answers and tool-use chains from LLaMA and ChatGPT. 

To run the ChatGPT evaluation code:
```bash
python toolbench/evaluation/evaluate_by_chatgpt.py
```

The evaluation prompt for ChatGPT is designed as follows:
```
You are a fair AI assistant for checking the quality of the answers of other two AI assistants. 

    [Question] 

    {data['query']}

    [The Start of Assistant 1's Answer]

    llama chains: {data['llama_chains']}
    llama answer: {data['llama_answer']}

    [The End of Assistant 1's Answer]

    [The Start of Assistant 2's Answer]

    chatgpt chains: {data['chatgpt_chains']}
    chatgpt answer: {data['chatgpt_answer']}

    [The End of Assistant 2's Answer] 

    We would like to request your feedback on the performance of two AI assistants in response to the user question displayed above. 
    Please first judge if the answer is correct based on the question, if an assistant gives a wrong answer, the score should be low.
    Please rate the quality, correctness, helpfulness of their responses based on the question.
    Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance, your scores should be supported by reasonable reasons. 
    Please first output a single line containing only two values indicating the scores for Assistant 1 and 2, respectively. 
    The two scores are separated by a space. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias, and the order in which the responses were presented does not affect your judgement.
    If the two assistants perform equally well, please output the same score for both of them.
```

The evaluation results for 15 cases for 6 tools are as below (higher is better), our ToolLLaMA matches or outperforms ChatGPT in different scenarios.

| Tool                            | ToolLLaMA Score         | ChatGPT Score         |
| ------------------------------- | ------------------- | --------------------- |
| baidu-translation               | 8.0                 | 8.0                   |
| chemical-prop                   | 7.93                | 7.53                  |
| bing-map                        | 7.93                | 7.64                  |
| stock                           | 4.87                | 4.4                   |
| weather                         | 7.20                | 7.47                  |
| wolframalpha                    | 7.67                | 7.80                  |

## TODO
- [ ] Release the rest part of the data for other tools in BMTools.
- [ ] ToolLLaMA will reach GPT-4's tool-use capability.
- [ ] There will be a Chinese version of ToolBench.
- [ ] Support Chinese LLMs, e.g., CPM-bee.

## Citation
Feel free to cite us if you like ToolBench.

```bibtex
@misc{qin2023tool,
      title={Tool Learning with Foundation Models}, 
      author={Yujia Qin and Shengding Hu and Yankai Lin and Weize Chen and Ning Ding and Ganqu Cui and Zheni Zeng and Yufei Huang and Chaojun Xiao and Chi Han and Yi Ren Fung and Yusheng Su and Huadong Wang and Cheng Qian and Runchu Tian and Kunlun Zhu and Shihao Liang and Xingyu Shen and Bokai Xu and Zhen Zhang and Yining Ye and Bowen Li and Ziwei Tang and Jing Yi and Yuzhang Zhu and Zhenning Dai and Lan Yan and Xin Cong and Yaxi Lu and Weilin Zhao and Yuxiang Huang and Junxi Yan and Xu Han and Xian Sun and Dahai Li and Jason Phang and Cheng Yang and Tongshuang Wu and Heng Ji and Zhiyuan Liu and Maosong Sun},
      year={2023},
      eprint={2304.08354},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
