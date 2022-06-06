
if __name__ == "__main__":
    dic_path = "./dict.txt.big.txt"
else:
    dic_path = "utils/dict.txt.big.txt"

# 导入分词词典
dic = {}
max_len = 0  # 最长词的长度
with open(dic_path, encoding="utf-8") as d:
    line = d.readline()
    while line:
        tmp_word = line.split()[0]
        word_len = len(tmp_word)
        max_len = max_len if max_len > word_len else word_len
        if dic.get(word_len):
            dic[word_len].add(tmp_word)
        else:
            dic[word_len] = {tmp_word}
        line = d.readline()


# 分词
def word_cut(l_sentence, english=False):
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
        index += l_word_len

        if english:
            # 保留英文
            # 对于字母和空格直接添加到tmp里面，防止一个英语单词被拆开
            if "a" <= l_tmp_word <= "z" or "A" <= l_tmp_word <= "Z" or l_tmp_word == " ":
                if len(tmp) > 0 and not ("a" <= tmp[-1] <= "z" or "A" <= tmp[-1] <= "Z" or tmp[-1] == " "):
                    tmp += " "
                tmp += l_tmp_word
                continue
        else:
            # 英文直接去掉
            if "a" <= l_tmp_word <= "z" or "A" <= l_tmp_word <= "Z" or l_tmp_word == " ":
                continue

        if index == 0:
            tmp += l_tmp_word
        else:
            tmp += " " + l_tmp_word

    l_sentence = tmp.strip()
    return l_sentence
