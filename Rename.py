# -*- coding=utf-8 -*


"""
由于下载的歌曲可能包含一些奇怪的名字，导致在U盘或者tf卡显示不正常，
所以将文件统一按00000~20000排号。
"""

import os
import argparse

file_handle = open('music_list_id.txt', mode='w')


def rename(root):
    FileLists = os.listdir(root)
    for filelist in FileLists:
        path = os.path.join(root, filelist)
        # print(filelist)
        if os.path.isfile(path):  # 文件
            if filelist.endswith('.mp3'):  # mp3 文件
                if os.path.getsize(path) // 1024 // 1024 == 0:
                    os.remove(path)
                    continue
                global ID
                new_file = os.path.join(root, '{:0>6d}.mp3'.format(ID))  # rename
                ID += 1  # ID +1 一定要有，否则白费
                os.rename(path, new_file)
                file_handle.write('{:0>6d}  {} \n'.format(ID, filelist))
                print(ID)
        elif os.path.isdir(path):
            rename(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename music file.')
    parser.add_argument("path", help="a root path to rename", type=str)
    parser.add_argument("id", help="a start id for rename", type=int)
    args = parser.parse_args()

    print('处理中。。。')
    ID = args.id
    rename(args.path)
    file_handle.close()
    print('完成')
