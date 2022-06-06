import os
import re
from pypinyin import lazy_pinyin, Style

FAB = 7  # 截取一个词前后FAB个长度

if __name__ == "__main__":
    input_path = "./data-1k"
    index = "./dic"
else:
    input_path = "utils/data-1k"
    index = "utils/dic"


# 输出文件夹
out_path = "\\".join(os.getcwd().split("\\")[:-1]) + "\\out"

# 建立一个所有文件的编号的字典
# 键：文件名（含后缀）；值：编号
file_id = {}

# 建立一个通过编号查找文件名的列表，含后缀，加个None用来占0位
id_file = [None]

files = os.listdir(input_path)
# files.sort(key=lambda x: [x.encode('gbk')])  # 根据GBK编码进行排序（有一点问题）
# 使用pypinyin包进行排序
files.sort(key=lambda x: lazy_pinyin(x, style=Style.TONE3))
i = 1
for f in files:
    file_id[f] = i
    id_file.append(f)
    i += 1

# print(id_file[1])

# 将得到的倒排索引导入成字典
# 键：词语（不含后缀名）；值：含有该词语的文件的编号所组成的列表
dic = {}
words = os.listdir(index)
for w in words:
    with open(index + "/" + w) as f:
        dic[w[:-4]] = list(map(lambda x: file_id[x.split()[0]], f.readlines()))


def inter(list1: list, list2: list):
    """
    交集的实现
    :param list1: 列表1
    :param list2: 列表2
    :return: list1 and list2
    """
    list1.sort()
    list2.sort()
    res = []
    i1 = 0
    i2 = 0
    while i1 < len(list1) and i2 < len(list2):
        if list1[i1] == list2[i2]:
            res.append(list1[i1])
            i1 += 1
            i2 += 1
        else:
            if list1[i1] > list2[i2]:
                i2 += 1
            else:
                i1 += 1
    return res


def union(list1: list, list2: list):
    """
    并集的实现
    :param list1: 列表1
    :param list2: 列表2
    :return: list1 or list2
    """
    list1.sort()
    list2.sort()
    res = []
    i1 = 0
    i2 = 0
    while i1 < len(list1) and i2 < len(list2):
        if list1[i1] < list2[i2]:
            res.append(list1[i1])
            i1 += 1
        elif list2[i2] < list1[i1]:
            res.append(list2[i2])
            i2 += 1
        else:
            res.append(list1[i1])
            i1 += 1
            i2 += 1
    if i1 < len(list1):
        res += list1[i1:]
    elif i2 < len(list2):
        res += list2[i2:]
    return res


def search(query: str):
    """
    实现复杂的查询（不带括号）
    :param query: 输入的查询语句
    :return: 查询结果列表以及输入的所有词语组成的列表所组成的一个长度为2的元组
    """
    query = query.split()  # 分割查询语句
    ret = dic.get(query[0], [])  # 查询结果列表
    input_words = [query[0]]  # 输入的所有词语列表

    for i in range(1, len(query)):
        if query[i] == "AND" or query[i] == "and":
            word_res = dic.get(query[i + 1], [])
            ret = inter(ret, word_res)
        elif query[i] == "OR" or query[i] == "or":
            word_res = dic.get(query[i + 1], [])
            ret = union(ret, word_res)
        else:
            input_words.append(query[i])

    return ret, input_words


def show(target_word: list, l_result: list):
    """
    将结果展示出来
    :param target_word: 目标词语组成的列表
    :param l_result: 交并操作后的文件id组成的列表
    :return: None
    """
    # out_f = open("{}/{}.txt".format(out_path, out_file_name), "wt", encoding="utf-8")
    # 构建一个正则表达式，用于查找一个词是否在一行中出现
    # cmp = re.compile(r"{}|{}".format(target_word[0], target_word[1]) if len(target_word)
    # == 2 else r"{}".format(target_word[0]))
    context = []
    cmp = ""
    length = len(target_word)
    for i in range(length):
        cmp += target_word[i] + ("|" if i < length - 1 else "")
    cmp = re.compile(cmp)
    for r in l_result:
        # 通过文件id找到文件名并打开相应的文件进行读取
        with open("{}/{}".format(input_path, id_file[r]), encoding="utf-8") as fo:
            # print(id_file[r] + "：")
            # out_f.write(id_file[r] + "：\n")
            line = fo.readline()
            while line:
                # 只看body部分
                if line.startswith("title"):
                    # 遇到title，跳到下面第二行
                    line = fo.readline()
                    line = fo.readline()
                    continue
                if line.startswith("link"):
                    break
                if cmp.findall(line):
                    # 建立一个迭代器，内容为找到的词
                    it = cmp.finditer(line)
                    over = False
                    head = 0
                    tmp = []
                    while not over:
                        try:
                            now = next(it)
                            start = now.start()
                            end = now.end()
                            tmp.append(line[head: start if start - head < 2 * FAB else (head + FAB) if head > 0 else head])
                            if start - head > 2 * FAB:
                                head = start - FAB
                                tmp.append("......" + line[head: start])
                            # 将查询词加重
                            tmp.append("#" + line[start: end] + "#")
                            head = end
                        except StopIteration:
                            # 迭代结束
                            # tmp.append(line[head: head + FAB] + "......" if head + FAB < len(line) else "")
                            tmp.append((line[head: head + FAB] + "......") if head + FAB < len(line) else line[end:])
                            line = "".join(tmp)
                            over = True
                    context.append(line[:-1])
                    # out_f.write(line[:-1] + "\n")
                line = fo.readline()
        # print()
        # out_f.write("\n")
    return context


def search_one_file(query: list, file_name: str):
    return show(query, [file_id[file_name]])


if __name__ == "__main__":
    # print(out_path)
    q1 = ["大小", "雏鸡"]
    q2 = ["斗争"]
    f_name = "各尽所能，按劳分配.txt"
    print(search_one_file(q1, f_name))
    # show(q, search("可爱 OR 美好 OR 美丽")[0])
