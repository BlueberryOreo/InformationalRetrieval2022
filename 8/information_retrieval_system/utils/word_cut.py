# 分词模块
import os
import re

# 判断文件位置
if os.getcwd().endswith("utils"):
    root = "./"
else:
    root = "utils/"

dic = {}
stopwords = {}
max_len = 0

# 初始化
# 建立分词词典
with open(root + "dict.txt.big.txt", encoding="utf-8") as f:
    line = f.readline()
    while line:
        word = line.split()[0]
        length = len(word)
        if dic.get(length):
            dic[length].add(word)
        else:
            dic[length] = {word}
        line = f.readline()

keys = list(dic.keys())
keys.sort(reverse=True)
max_len = keys[0]

# 建立废弃单词词典
stopwords_file_lst = os.listdir(root + "stopwords-master")
for f in stopwords_file_lst:
    if not f.endswith(".txt"):
        continue
    file_name = root + "stopwords-master/" + f
    with open(file_name, encoding="utf-8") as ff:
        line = ff.readline()
        while line:
            word = line.strip()
            length = len(word)
            if stopwords.get(length):
                stopwords[length].add(word)
            else:
                stopwords[length] = {word}
            line = ff.readline()


def english_cut(s: str, start: int):
    en_word = ""
    i = start
    while i < len(s) and ('a' <= s[i] <= 'z' or 'A' <= s[i] <= 'Z'):
        en_word += s[i]
        i += 1
    if i < len(s) and s[i] == ' ':
        i += 1
    return en_word, i


# 针对一个文件的分词，带有计算wtd的功能
def word_cut_file(l_sentences: list, need_cnt=True, english=False):
    word_cnt = {}  # 用于记录该文件中每个词出现的次数
    for i in range(len(l_sentences)):
        tmp = ""
        index = 0
        # english_cnt = 0
        while index < len(l_sentences[i]):
            # print(dic)
            word_len = max_len
            while l_sentences[i][index: index + word_len] not in dic[word_len]:
                word_len -= 1
                if word_len == 1:
                    break
            tmp_word = l_sentences[i][index: index + word_len]

            if "a" <= tmp_word <= "z" or "A" <= tmp_word <= "Z":
                tmp_word, index = english_cut(l_sentences[i], index)
                # index += 1

                if not english:
                    continue
            elif (stopwords.get(word_len) and tmp_word in stopwords[word_len]) or (
                    re.findall(r"[\\/:*?\"<>|]", tmp_word)):
                # 剔除废弃词语、非法符号
                index += word_len
                continue
            else:
                index += word_len
            if not tmp_word.strip():
                continue
            # 分词
            # if dic == 0 or "a" <= tmp_word <= "z" or "A" <= tmp_word <= "Z":
            # 记录词个数
            if word_cnt.get(tmp_word):
                word_cnt[tmp_word] += 1
            else:
                word_cnt[tmp_word] = 1

            if index == 0:
                tmp += tmp_word
            else:
                tmp += " " + tmp_word
        l_sentences[i] = tmp.strip()
    return (l_sentences, word_cnt) if need_cnt else l_sentences


# 针对一句话的分词
def word_cut_sentence(l_sentence, english=False):
    tmp = ""
    index = 0
    while index < len(l_sentence):
        # print(dic)
        l_word_len = max_len
        while l_sentence[index: index + l_word_len] not in dic[l_word_len]:
            l_word_len -= 1
            if l_word_len == 1:
                break
        l_tmp_word = l_sentence[index: index + l_word_len]
        flag = False

        if english:
            # 保留英文
            # 对于字母和空格直接添加到tmp里面，防止一个英语单词被拆开
            if "a" <= l_tmp_word <= "z" or "A" <= l_tmp_word <= "Z" or l_tmp_word == " ":
                l_tmp_word, index = english_cut(l_sentence, index)
                flag = True
                # if len(tmp) > 0 and not ("a" <= tmp[-1] <= "z" or "A" <= tmp[-1] <= "Z" or tmp[-1] == " "):
                #     tmp += " "
                # tmp += l_tmp_word
                # continue
        else:
            # 英文直接去掉
            if "a" <= l_tmp_word <= "z" or "A" <= l_tmp_word <= "Z" or l_tmp_word == " ":
                index += l_word_len
                continue

        index += l_word_len if not flag else 0

        if index == 0:
            tmp += l_tmp_word
        else:
            tmp += " " + l_tmp_word

    l_sentence = tmp.strip()
    return l_sentence


if __name__ == '__main__':
    print(word_cut_sentence("computer science", True))
    print(word_cut_file(open("D:\\info.txt").readlines(), english=True))
