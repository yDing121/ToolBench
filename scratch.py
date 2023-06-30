# import openai
#
#
# prompt = "Tell me what you know about OpenAI"
# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a friendly AI assistant"},
#         {"role": "user", "content": prompt},
#     ],
#     max_tokens=1024
# )
import json


with open("./data-generation/queries/response.txt", "r") as fin:
    response = "".join(fin.readlines())
    print(response)


response = json.loads(response)["choices"][0]["message"]["content"]
print("cleaned response:\n\n\n" + response)