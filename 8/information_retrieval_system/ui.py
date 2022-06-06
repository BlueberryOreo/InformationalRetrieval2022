# UI
import _tkinter
import os
import sys
from tkinter import *
from tkinter import messagebox, scrolledtext
from tkinter.ttk import Progressbar
from utils.fonts import *

from utils import *
import creeper


max_line = 30
max_len = 60
out_path = "{}\\utils\\websites".format(os.getcwd())
html_out_path = "{}\\utils\\htmls".format(os.getcwd())
test_out = "./test_creep/websites"
test_html = "./test_creep/htmls"
DEBUG = False


def unpack(res: list):
    ret = []
    tmp = ""
    line = 0
    for r in res:
        # print(len(tmp.split("\n")))
        # if len(tmp.split("\n")) >= max_line:
        #     ret.append(tmp)
        #     tmp = ""
        if r.split()[-1].startswith("Sim"):
            r = ">>>" + r.split()[0]
            if tmp:
                tmp += "\n"
                line += 1
        i = 0
        while i < len(r):
            tmp += r[i: i + max_len] + "\n"
            line += 1
            if line >= max_line:
                ret.append(tmp)
                tmp = ""
                line = 0
            i += max_len
    if tmp:
        ret.append(tmp)
    return ret


def quit_progress():
    exit(0)


class MainWindow:
    height = 660
    width = 980
    frame_width = 100
    res = []
    now = 0
    title = "锑度"

    def __init__(self):
        self.cw = None
        self.window = Tk()
        self.window.geometry("{}x{}".format(self.width, self.height))
        self.window.title(self.title)
        self.window.protocol("WM_DELETE_WINDOW", quit_progress)
        # self.window.resizable(width=False, height=False)

        """
            创建三个Frame，一个用于放其他按钮，一个用于放文本框和检索按钮，一个用于放结果展示的label
        """
        self.else_frame = Frame(self.window, bg="lightblue")
        self.retrieval_frame = Frame(self.window, bg="green")
        self.show_frame = Frame(self.window, bg="yellow")

        self.else_frame.pack(side="left", fill=Y)
        self.retrieval_frame.pack(side="top", fill=X)
        self.show_frame.pack(expand=True, fill=BOTH)
        # self.show_frame.pack(side="right", anchor="s", fill=X)

        """
            其他框中的组件：
                提示Label
                清空当前输入
                重新爬取网页按钮
                更新倒排索引按钮
        """
        self.else_label = Label(self.else_frame, text="其他", font=(hei, 15), bg="lightblue")
        self.clear_bt = Button(self.else_frame, text="清空", font=(song, 12),
                               command=self.clear_clicked)
        self.creep_bt = Button(self.else_frame, text="更新网页", font=(song, 12), command=self.creep_clicked)
        self.invert_index_bt = Button(self.else_frame, text="更新倒排", font=(song, 12), command=self.invert_clicked)
        self.else_label.pack(pady=10, padx=10, fill=X)
        self.clear_bt.pack(pady=10, padx=10, fill=X)
        self.creep_bt.pack(pady=10, padx=10, fill=X)
        self.invert_index_bt.pack(pady=10, padx=10, fill=X)

        if DEBUG:
            self.test_bt = Button(self.else_frame, text="测试", command=lambda: print("测试测试"))
            self.test_bt.pack(pady=10, padx=10, fill=X)

        """
            检索框中的组件
                输入查询语句用的Entry
                检索按钮
        """
        self.query_text = Entry(self.retrieval_frame, font=(hei, 15), width=70)
        self.retrieval_bt = Button(self.retrieval_frame, text="检索", font=(song, 15),
                                   command=self.retrieval_clicked)
        self.query_text.focus()
        self.query_text.pack(pady=10, side="left", expand=True)
        self.retrieval_bt.pack(pady=10, side="left", expand=True)

        """
            展示框中的组件
                用于展示结果的Label
                用于翻页的两个按钮
                显示当前页面和总页面的Label
        """
        # self.result_text = StringVar()  # 用于改变result的内容
        self.result = Label(self.show_frame,
                            font=(song, 13), bg="white",
                            anchor="nw", justify=LEFT)  # wraplength=700 wraplength: 超过这个像素长度就自动换行
        self.page_up = Button(self.show_frame, font=(song, 12), text="上一页",
                              command=self.page_up_clicked,
                              state=DISABLED)
        self.page_down = Button(self.show_frame, font=(song, 12), text="下一页",
                                command=self.page_down_clicked,
                                state=DISABLED)
        self.page = Label(self.show_frame, font=(song, 12), text="第0页，共0页", bg="yellow")
        self.result.pack(expand=True, fill=BOTH)
        self.page_up.pack(side="left", anchor="s", pady=10, expand=True)
        self.page.pack(side="left", anchor="s", pady=10, expand=True)
        self.page_down.pack(side="left", anchor="s", pady=10, expand=True)

        self.window.mainloop()

    def retrieval_clicked(self):
        """
        检索
        :return:
        """
        self.init()
        query = self.query_text.get()
        # self.result.config(text=query)
        res, state = tf_idf.run(query)
        hint = res[-1]
        if state:
            messagebox.showinfo("提示", hint)
            self.res = unpack(res[:-1])
            self.result.config(text=self.res[self.now])
            self.page.config(text="第{}页，共{}页".format(self.now + 1, len(self.res)))
            if len(self.res) > 1:
                self.page_down.config(state=NORMAL)
            # for r in self.res:
            #     print(r)
            #     print("===================================")
        else:
            messagebox.showinfo("注意", hint)
            self.clear_clicked()

    def page_down_clicked(self):
        """
        下一页
        :return:
        """
        self.now += 1
        if self.now > 0:
            self.page_up.config(state=NORMAL)
        self.page.config(text="第{}页，共{}页".format(self.now + 1, len(self.res)))
        self.result.config(text=self.res[self.now])
        if self.now == len(self.res) - 1:
            self.page_down.config(state=DISABLED)

    def page_up_clicked(self):
        """
        上一页
        :return:
        """
        self.now -= 1
        if self.now < len(self.res) - 1:
            self.page_down.config(state=NORMAL)
        self.page.config(text="第{}页，共{}页".format(self.now + 1, len(self.res)))
        self.result.config(text=self.res[self.now])
        if self.now == 0:
            self.page_up.config(state=DISABLED)

    def init(self):
        """
        初始化res, now, page, page_up, page_down
        :return:
        """
        self.res = []
        self.now = 0
        self.page.config(text="第{}页，共{}页".format(self.now, len(self.res)))
        self.page_up.config(state=DISABLED)
        self.page_down.config(state=DISABLED)

    def clear_clicked(self):
        """
        清空按钮被点击
        :return:
        """
        self.init()
        self.result.config(text="")
        self.query_text.delete(0, END)

    def creep_clicked(self):
        # messagebox.showinfo("信息", "该功能尚未完成，敬请期待")
        self.clear_clicked()
        try:
            self.cw = CreepWindow()
        except _tkinter.TclError as e:
            print(e)

    def invert_clicked(self):
        req = messagebox.askyesno("确认操作", "确认更新倒排吗？")
        if not req:
            return
        self.clear_clicked()
        messagebox.showwarning("注意", "更新倒排需要一点时间，程序可能会暂时未响应，请耐心等待！")
        self.window.title("{}（{}）".format(self.title, "更新倒排中..."))
        invert_index.run("./utils/websites")
        bool_query.update()
        tf_idf.update()
        messagebox.showinfo("信息", "更新完成！")
        self.window.title(self.title)


class CreepWindow:
    """
        基本完成
    """
    height = 300
    width = 400

    def __init__(self):
        self.window = Toplevel()
        self.window.geometry("{}x{}".format(self.width, self.height))
        self.window.title("爬虫")
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)

        """
            设置Frame
                组件：说明Label，输入网址的Entry，说明爬多少个网站的Label，选择网站数目的Spinbox，是否全部爬取Checkbutton，开始按钮
        """
        self.settings_frame = Frame(self.window)
        self.explain_lab = Label(self.settings_frame, text="请输入要爬取的网站的根网址", font=(song, 15))
        self.web_path = Entry(self.settings_frame, width=40, font=(hei, 13))
        self.web_num_lab = Label(self.settings_frame, text="请选择需要爬取多少个网站", font=(song, 15))
        # self.var = IntVar()
        # self.var.set(1000)
        self.web_num = Spinbox(self.settings_frame, from_=0, to=5000, width=5, font=(hei, 15))
        self.creep_all_var = BooleanVar()
        self.creep_all_var.set(False)
        self.creep_all = Checkbutton(self.settings_frame, text="全部爬取",
                                     variable=self.creep_all_var, command=self.is_creep_all)
        self.start_bt = Button(self.settings_frame, text="开始", font=(song, 15), command=self.start_clicked)
        self.explain_lab.pack(pady=10)
        self.web_path.pack(pady=10)
        self.web_num_lab.pack(pady=10)
        self.web_num.pack(pady=10)
        self.creep_all.pack(pady=10)
        self.start_bt.pack(pady=10)

        self.settings_frame.pack()

        """
            进度Frame
                组件：进度条，显示已经爬取的网站的scrolledtext
        """
        self.progress_frame = Frame(self.window)
        self.progress = Progressbar(self.progress_frame, maximum=100, length=self.width)
        self.info = scrolledtext.ScrolledText(self.progress_frame, state=DISABLED)
        # bt = Button(self.progress_frame, text="点我测试", command=self.test_clicked)
        self.redirect = Redirect(self.info)
        sys.stdout = self.redirect  # 将输出重定向到info上
        self.progress.pack()
        self.info.pack(fill=X)
        # bt.pack()

        self.window.mainloop()

    def is_creep_all(self):
        # print(self.creep_all_var.get())
        if self.creep_all_var.get():
            self.web_num.config(state=DISABLED)
        else:
            self.web_num.config(state=NORMAL)

    def start_clicked(self):
        # print(self.creep_all_var.get())
        # print(int(self.web_num.get()) if not self.creep_all_var.get() else -1)
        path = out_path
        html_path = html_out_path
        # path = test_out
        # html_path = test_html
        req = messagebox.askyesno("注意", "爬取的网站会存放到{}文件夹中，并且会覆盖原已爬取的网站\n"
                                        "是否要爬取？".format(path))
        if not req:
            self.window.attributes("-topmost", True)
            return
        self.window.attributes("-topmost", True)
        self.settings_frame.pack_forget()
        self.progress_frame.pack()
        self.window.update()
        url = self.web_path.get()
        num = int(self.web_num.get()) if not self.creep_all_var.get() else -1
        # if num > 5000:
        #     num = 5000
        # print(num)
        creeper.bfs(url, num, path, html_path, self.progress)
        if self.progress["value"] != self.progress["maximum"]:
            self.progress["value"] = self.progress["maximum"]
        self.window.attributes("-topmost", False)
        messagebox.showinfo("信息", "爬取完毕！\n请及时更新倒排！")
        self.destroy()

    def destroy(self):
        self.redirect.restore_std()  # 恢复标准输出
        self.window.destroy()

    # def test_clicked(self):
    #     print("this hello")
    #     creeper.test_print()


class Redirect:
    """
        重定向类，将stdout重定向到tkinter的组件中
    """

    def __init__(self, widget):
        self.out = widget
        # 标准输出途径备份
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr

    def write(self, *info):
        info = list(map(str, info))
        self.out.config(state=NORMAL)
        self.out.insert("end", " ".join(info))
        # self.out.insert("end", "\n")
        self.out.see("end")
        self.out.config(state=DISABLED)
        self.out.update()

    def restore_std(self):
        """
        恢复标准输出
        :return:
        """
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

    def flush(self):
        pass


if __name__ == "__main__":
    MainWindow()
    # CreepWindow()
