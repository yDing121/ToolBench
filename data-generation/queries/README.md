## 使用指导

须填写相关管工具的的description和query示例到tool_descriptions.json和seed_data/**.txt

tool_descriptions里推荐包含的内容：这个tool整体的目的/需求，支持的函数以及每个函数的对应功能（可以直接从对应的api.py里复制），核心函数的返回结果示例（方便chatgpt反向构造）

seed_data/tool_name.txt, 一行一个人工写的query，让chatgpt通过in-context learning构造数据，原则上用户自己写的真实数据，需要提供足够多样的数据，数据量最好>100条。

然后可以运行generate_queries.sh脚本获取数据

数据将保存在output文件夹对应的tool_name文件夹下，可以通过'python deduplication.py --file_path 'your_file_path' '来去重该文件(默认bash脚本中自动运行)
