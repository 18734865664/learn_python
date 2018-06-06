#! /usr/local/python3/bin/python3
#  encoding:utf8

import re


lst = ["bat", "bot", "but", "hat", "hit", "hut"]
pillar = re.compile(r"正则表达式", re.M|re.I)


def check_lst(lst):
    for i in lst:
        print(i)
        try:
            print(re.match(pillar, i).group())
        except Exception:
            print("未匹配到")
        else:
            print("匹配成功")
        print("++" * 20)


str_demo = input("写点啥：")
try:
    print(re.search(pillar, str_demo).group())
except:
    print("没有")
else:
    print("有")

        



