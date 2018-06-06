#!/bin/env python
# -*- coding: utf-8 -*-
import sys, time

reload(sys)
sys.setdefaultencoding("utf-8")
from pygit2 import *
from datetime import datetime


def timestampToDatetime(timestamp):
    timestamp = float(timestamp);
    return datetime.fromtimestamp(timestamp)


def Commit_Log(repo):
    repo = Repository(repo)
    counts = 0
    commit_list = []
    for commits in repo.walk(repo.head.target, GIT_SORT_TIME):
        if counts < 20:
            commit_dict = {}
            commit_dict['commit_id'] = str(commits.id)[0:7]
            commit_dict['commit_author'] = str(commits.author.name)
            commit_dict['commit_message'] = str(commits.message)
            commit_dict['date_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(commits.commit_time))
            commit_list.append(commit_dict)
            counts += 1
    return commit_list


def resetLog(oid, repo):
    repo = Repository(repo)
    repo.reset(oid, GIT_RESET_SOFT)


if __name__ == '__main__':
    path = "/data/ngx_openresty/nginx/html/api-juzi/.git"
    repo = path
    print Commit_Log(repo)
