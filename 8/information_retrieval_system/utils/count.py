import os
import json
import re

root = "./websites/"
webs = os.listdir(root)
# print(webs)
sentences = 0
index = dict(json.load(open("./index.json", encoding="utf-8")))
patch = re.compile(r"[。？！.\s]")
for w in webs:
    try:
        with open(root + w, encoding="utf-8") as f:
            lines = " ".join(f.read().split("\n"))
            sentences += len(patch.split(lines))
    except FileNotFoundError:
        pass

print("总共爬取到{}个网页".format(len(index["file_id"])))
print("总句子数量为{}句".format(sentences))
print("一共有{}个词".format(len(index["words"])))

os.system("pause")
"""
总共爬取到3022个网页
总句子数量为1341899句
一共有39453个词
"""