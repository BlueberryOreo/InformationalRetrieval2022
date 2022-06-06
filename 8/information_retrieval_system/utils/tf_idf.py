# 网页排序模块
import os
import json
from math import log10, sqrt

if __name__ == "__main__":
    from word_cut import word_cut_sentence
    from bool_query import search_one_file
else:
    from .word_cut import word_cut_sentence
    from .bool_query import search_one_file

# print(words_id)

if os.getcwd().endswith("utils"):
    input_path = "./websites"
    index = "./index.json"
    output_path = "\\".join(os.getcwd().split("\\")[:-1] + ["out"])
else:
    input_path = "utils/websites"
    index = "utils/index.json"
    output_path = "{}\\out".format(os.getcwd())

N = 0
word_id = {}  # 键：词语；值：词语的序号
dic = {}


def update():
    global N
    global dic
    # 导入倒排所得文件名并序列化
    # g_words = os.listdir("./{}".format(dic))
    jdic = dict(json.load(open(index, encoding="utf-8")))
    dic = dict(jdic["words"])  # 倒排，{词: {id, file_name, wtd, d}}
    N = len(jdic["file_id"])  # 总网页文件数

    dkeys = list(dic.keys())
    # print(dkeys)
    NN = len(dkeys)
    for i in range(NN):
        word = dkeys[i]
        word_id[word] = i


def idf(words: list):
    """
    处理query词向量：倒排索引中不存在的去掉（原位置换成0），存在的原位置换成一个长度为2的元组，第一个值是词语: str，第二个值是这个词的idf: float
    :param words: query词向量
    :return: 处理后的query词向量
    """
    l = len(words)
    ret = []  # 每个元素是一个长度为2的元组，第一个值是词语: str，第二个值是idf: float
    for i in range(l):
        if word_id.get(words[i]):
            # 词存在
            # with open("./{}/{}.txt".format(invert_dir, words[i])) as f:
            #     # 计算这个词在多少个文档中出现过
            #     dft = len(f.read().strip().split("\n"))
            dft = len(dic[words[i]])
            ret.append((words[i], log10(N / dft)))
        else:
            ret.append(0)
    return ret


# 用于存储找到的网页文件。键：文件名；值：一个长度为2的列表。第一个值是cos的分子，第二个值是文件词向量的长度。最后将会被转化成一个cos值
file_list = {}


def find(words: list):
    """
    根据query词向量中的词通过倒排索引找出包含该词的网页文件，并且计算出对应文件词向量的模的平方以及和query词向量之间的cos值的分子
    :param words: 处理后的query词向量
    :return:
    """
    for w in words:
        if w:
            # print(w)
            for f in dic[w[0]]:
                file = f["file_name"]
                wtd = f["wtd"]
                l_d = f["d"]
                if file_list.get(file):
                    # print(file_list[file], w[1])
                    file_list[file][0] += wtd * w[1]
                else:
                    file_list[file] = [wtd * w[1], l_d]


def get_query_len(words: list):
    """
    计算query词向量的长度
    :param words: 处理后的query词向量
    :return: query词向量的长度
    """
    ret = 0
    for w in words:
        if w:
            ret += w[1] ** 2
    if ret < 1e-5:
        # 0向量（输入的词存在的词在所有文件中都出现过）
        return 1.0
    return sqrt(ret)


def cos_calc(l_q_len: float):
    """
    将file_list中的值计算成cos值
    :param l_q_len: query词向量的长度
    :return:
    """
    l_keys = file_list.keys()
    for k in l_keys:
        # print(file_list[k][1], l_q_len)
        file_list[k] = file_list[k][0] / (file_list[k][1] * l_q_len)


def run(query: str):
    # 对输入进行分词并切割成列表
    q_words = word_cut_sentence(query, english=True).split()
    # print(q_words)

    # 处理得到query词向量，将其中的词转换成对应的idf
    q_words = idf(q_words)
    # print(q_words)

    # 利用倒排索引通过query词向量找出含有这些词的文件，并且计算出对应文件词向量的模的平方以及和query词向量之间的cos值的分子
    # 为后续cos的计算做准备
    find(q_words)

    # print(file_list)

    # 获得query词向量的长度
    q_len = get_query_len(q_words)
    # print(q_len)

    # 计算出对应文件词向量和query词向量的cos值
    cos_calc(q_len)

    # print(file_list)

    keys = list(file_list.keys())

    # 根据cos值进行排序
    keys.sort(key=lambda k: file_list[k], reverse=True)
    res = []

    if keys:
        file = open("{}\\{}.txt".format(output_path, query), "wt", encoding="utf-8")
        for k in keys:
            res.append("{} Sim={:.5f}".format(k, file_list[k]))
            file.write("{} Sim={:.5f}\n".format(k, float(file_list[k])))
            # print(r_q_words, k)
            r_q_words = []
            for q in q_words:
                if q:
                    r_q_words.append(q[0])
            context = search_one_file(r_q_words, k)
            # print(k)
            for c in context:
                res.append(c)
                file.write(c + "\n")
            file.write("\n")
        # file.write("\n".join(res) + "\n")
        file.flush()
        file.close()
        res.append("结果已保存到”{}\\{}.txt“文件中！".format(output_path, query))
        state = 1
    else:
        res.append("未找到相关内容！")
        state = 0

    # 一次查询结束后清空file_list
    file_list.clear()
    return res, state
    # print("\n")
    # query = input("请输入需要查找的语句（输入###退出交互）：")


update()

if __name__ == "__main__":
    query = "computer science"
    ret = run(query)
    for r in ret:
        print(r)
    pass
