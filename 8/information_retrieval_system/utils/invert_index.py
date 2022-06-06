# 倒排索引模块
import os
import re
import math
from tkinter.ttk import Progressbar
if __name__ == "__main__":
    import word_cut
else:
    from . import word_cut
import json

# 判断文件位置
if os.getcwd().endswith("utils"):
    root = "./"
else:
    root = "utils/"

res = {}
words_dic = {}
file_id = {}
used = {}


# 分句
def sentence_divide(l_file_path: str):
    l_f = open(l_file_path, encoding="utf-8")
    lines = l_f.readlines()
    # return lines
    l_sentences = []
    split_match = re.compile(r"[\n\s。！？]")
    for l in lines:
        context = re.split(split_match, l)
        if context[0] == 'body:' or context[0] == 'title:':
            continue
        # 去除link部分
        if context[0] == 'link:':
            break
        for c in context:
            if c:
                l_sentences.append(c)
    return l_sentences


# 倒排（修改后）
def invert(l_sentences, l_file_name, index):
    # visited = set()
    # 计算一个文件的词向量的长度
    d = 0
    for s in l_sentences[1].values():
        wtd = 1 + math.log10(s) if s > 0 else 0
        d += wtd ** 2
    d = math.sqrt(d)
    # print(d)
    for s in l_sentences[0]:
        words = set(s.split())
        for w in words:
            tf = l_sentences[1].get(w)  # 得到一个词在这个文档中出现的次数
            wtd = 1 + math.log10(tf) if tf > 0 else 0
            context = {"id": index, "file_name": l_file_name,
                       "wtd": float("{:.3f}".format(wtd)),
                       "d": float("{:.3f}".format(d))}
            if words_dic.get(w):
                if context["file_name"] in used[w]:
                    continue
                used[w].add(context["file_name"])
                words_dic[w].append(context)
            else:
                words_dic[w] = [context]
                used[w] = {context["file_name"]}


def run(dir_path: str, bar: Progressbar = None):
    file_list = os.listdir(dir_path)
    cnt = 0
    total = len(file_list)
    # info = ""
    for i in range(len(file_list)):
        # 进度
        # print("\b" * len(info), end="")
        cnt += 1
        # print(cnt)
        if bar:
            print(cnt)
            bar["value"] = cnt / total * 100
            bar.update()
        # info = "Solved:{:.1f}%".format(cnt / total * 100)
        # print(info, end="")
        # if f.startswith("阿"):
        if not file_list[i].endswith(".txt"):
            # 不是txt文件，跳过
            # total -= 1
            continue
        # f：文件名
        file_path = dir_path + "\\" + file_list[i]
        sentences = sentence_divide(file_path)
        # print(sentences)
        after_s = word_cut.word_cut_file(sentences, english=True)
        # print(after_s)
        invert(after_s, file_list[i], i)
        file_id[file_list[i]] = i

    with open(root + "index.json", "wt", encoding="utf-8") as index:
        """
        json文件格式：
        file_id: {文件对应编号},
        words: 
        {
            词语: 
            {
                id: 文件序号, 
                file_name: 文件名, 
                wtd, 
                d:文件词向量长度
            },
            ...
        }
        """
        res["file_id"] = file_id
        res["words"] = words_dic
        # j_res = json.dumps(res, sort_keys=True, indent=1, separators=(",", ":"), ensure_ascii=False)
        j_res = json.dumps(res, ensure_ascii=False)
        index.write(str(j_res))


if __name__ == "__main__":
    # dir_path = input("请输入需要倒排的文件所在的文件夹绝对路径：")
    # while not os.path.exists(dir_path):
    #     dir_path = input("输入的文件夹不存在！请重新输入：")
    # dir_out = input("请输入倒排存储的文件夹绝对路径：")
    # while not os.path.exists(dir_out):
    #     dir_out = input("输入的文件夹不存在！请重新输入：")
    path = "./websites"
    run(path)

