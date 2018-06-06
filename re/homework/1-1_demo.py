#! /usr/local/python3/bin/python3
#  encoding:utf8

import re


lst = ["bat", "bot", "but", "hat", "hit", "hut"]
pillar = re.compile(r"[bh][aiu]t", re.M|re.I)


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
        



if __name__ == "__main__":
    check_lst(lst)
