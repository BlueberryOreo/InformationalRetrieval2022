# from utils import *
#
#
# # 控制台运行版本，需要导入utils中的部分模块
# query = input("请输入查询语句（输入###退出交互）：")
# while query != "###":
#     # print(tf_idf.run(query))
#     res, state = tf_idf.run(query)
#     for r in res:
#         print(r)
#     print("\n")
#     query = input("请输入查询语句（输入###退出交互）：")

if __name__ == "__main__":
    import ui
    # UI运行版本
    ui.MainWindow()
