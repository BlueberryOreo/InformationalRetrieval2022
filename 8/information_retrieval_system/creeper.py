# 爬虫模块
import requests
import time
import queue
import re
import os
from tkinter.ttk import Progressbar

from utils.web_extract import Web

# cnt = 0
visited = set()
result = []
exist = {}
# root_url2 = "http://scst.suda.edu.cn/"


def init():
    global visited
    global result
    global exist
    visited = set()
    result = []
    exist = {}


def creeper(l_url: str, encoding: str):
    """
    爬虫
    :param l_url: 网址
    :param encoding: 编码
    :return: 如果成功爬到网站，则返回该response；如果失败超过50次，返回-1
    """
    repeat = 0
    while True:
        try:
            time.sleep(0.2)
            response = requests.get(l_url, timeout=10)
            response.encoding = encoding
            return response
        except Exception as e:
            # 出现异常，如请求超时、SSL错误等，重试
            repeat += 1
            print(e, "--Retry for {} time(s)".format(repeat))
            if repeat == 50:
                return -1


def output(dir_path: str, w: Web, html_path: str):
    file_name = re.sub(r"[\\/:*?\"<>|]", "_", w.get_title())  # 处理有特殊符号的文件名
    out_file_path = dir_path + "/" + file_name + str(exist.get(file_name, "")) + ".txt"
    html_out_path = html_path + "/" + file_name + str(exist.get(file_name, "")) + ".html"
    if exist.get(file_name):
        # 处理同名文件
        exist[file_name] += 1
    else:
        exist[file_name] = 1

    with open(html_out_path, "wt", encoding="utf-8") as out:
        out.write(w.text)
    with open(out_file_path, "wt", encoding="utf-8") as out:
        title = w.get_title()
        body = w.get_body()
        link = w.get_link()
        out.write("title:\n" + title + "\n")

        out.write("\n")
        out.write("body:\n")
        l_cnt = 0
        is_first = True
        for t in body:
            if t:
                out.write(t + "\n" if t else "")
                l_cnt = 0
            else:
                if l_cnt:
                    continue
                else:
                    l_cnt += 1
                    if is_first:
                        is_first = False
                        continue
                    out.write("\n")

        out.write("link:\n")
        for l in link:
            if l:
                try:
                    out.write(l[0] + " " + l[1] + "\n")
                except KeyError:
                    pass


def bfs(root_url: str, amount: int, output_path: str, html_path: str, progress: Progressbar = None):
    """
    使用bfs来爬取网页，并将网页正文提取出来，输出到指定文件中
    :param root_url: 根路径
    :param amount: 需要爬取的网页的数量，传入-1表示全部爬取
    :param output_path: 输出的文件夹路径
    :param html_path: 输出存储html文件的路径
    :param progress: 进度条组件
    :return: None
    """
    init()
    cnt = 0
    q = queue.Queue()
    if root_url.endswith("/"):
        root_url = root_url[:-1]
    q.put(root_url)

    # print("cnt={}, amount={}".format(cnt, amount), q.empty())

    while not q.empty():
        now_url = q.get()
        if now_url in visited or not now_url.startswith(root_url):
            # 已经访问过或者不是本站的网页
            continue

        response = creeper(now_url, "utf-8")
        if response == -1:
            # 爬取失败
            print("Fail to creep", now_url)
            continue
        visited.add(now_url)
        if 400 <= response.status_code <= 600:
            # 网站错误
            print(now_url, "**ERROR**", "status:", response.status_code)
            continue

        w = Web(response.text)
        # print(response.status_code)
        print(response.status_code, now_url, w.get_title())
        output(output_path, w, html_path)
        result.append(now_url)
        cnt += 1
        if progress:
            tmp = amount if amount != -1 else 2000
            if cnt / tmp * 100 > 100:
                progress["value"] = 99
            else:
                progress["value"] = cnt / tmp * 100
            progress.update()
        if cnt == amount:
            break

        links = w.get_link()
        for l in links:
            if l[1].startswith("http") or l[1].startswith("https"):
                # 绝对路径
                link = l[1]
            else:
                # 相对路径，改成绝对路径
                link = root_url + ("" if l[1].startswith("/") else "/") + l[1]

            if (".html" in link) or (".htm" in link):
                q.put(link)


def run(url: str, amount: int, output_dir_path: str, html_path: str):
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    if not os.path.exists(html_path):
        os.mkdir(html_path)
    bfs(url, amount, output_dir_path, html_path)


def test_print():
    print("hello")


if __name__ == "__main__":
    # url1 = "https://codeforces.com/"
    root_url2 = input("请输入要爬取的网站的根网址：")
    num = int(input("请输入要爬取的网页个数：（若全部爬取请输入-1）"))
    run(root_url2, num, "./utils/websites", "./utils/htmls")
    # print(websites)
