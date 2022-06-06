# 网页正文提取模块
from bs4 import BeautifulSoup


class Web:
    def __init__(self, html: str):
        """
        解析一个html（直接形式）
        :param html: 网页文件内容
        """
        self.text = html
        self.soup = BeautifulSoup(html, "html.parser")

    def get_title(self):
        return self.soup.title.text

    def get_body(self):
        return list(map(str.strip, self.soup.body.text.split("\n")))

    def get_link(self):
        links = self.soup.find_all("a")
        ret = []
        for link in links:
            if link.get("href"):
                ret.append((link.text.strip(), link["href"]))
        return ret


if __name__ == "__main__":
    web = open("/作业/4/example/ir-2022-spring-1.html", encoding="utf-8").read()
    # print(web)
    w = Web(web)
    # print(w.get_link())
    # print(w.get_body())
    print(w.get_link())
