#! /usr/local/python3/bin/python3
# encoding: utf-8

import os



class getFileList():

    def __init__(self, path):
        self.path = path

    def get_file_list(self):
        file_list = os.listdir(self.path)
        file_list_tmp = []
        for file_index in range(len(file_list)):
            if not 'bak' in file_list[file_index] and not "pipeline" in file_list[file_index] and not "test" in file_list[file_index] and  not "change" in file_list[file_index] and not 'zb' in file_list[file_index]:
                file_list_tmp.append(file_list[file_index])
        file_list = file_list_tmp.copy()
        #import pdb; pdb.set_trace()
        file_list_tmp.clear()
        return file_list


if __name__ == "__main__":
    obj = getFileList("/data/nfs/jenkins/jobs")
    print(obj.get_file_list())

        
