# -*- coding:utf-8 -*-
import os
import sys
import time

from PyPDF2 import PdfFileMerger

try:
    import configparser
except ImportError:
    import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

config_file = os.path.dirname(__file__) + '/merge.config'

try:
    config = configparser.ConfigParser()
except Exception as e:
    config = ConfigParser.ConfigParser()

config.read(config_file, encoding='utf-8')
format = '.pdf'


# 指定文件夹内所有pdf文档合并
def mergeDirFiles():
    # 单个目录
    dir = None
    dir_dest_dir = None
    dir_dest_name = None
    # 获取对应的节点信息
    if config.has_section('dir'):
        if config.has_option('dir', 'dir'):
            dir = config.get('dir', 'dir')
        if config.has_option('dir', 'dest_dir'):
            dir_dest_dir = config.get('dir', 'dest_dir')
        if config.has_option('dir', 'dest_name'):
            dir_dest_name = config.get('dir', 'dest_name')
    # 对节点信息进行异常兼容处理
    if dir == None or dir == '':
        return
    if not os.path.exists(dir):
        return
    if dir_dest_dir == None or dir_dest_dir == '':
        # 默认输出到当前目录
        dir_dest_dir = os.path.dirname(__file__)
    if not os.path.exists(dir_dest_dir):
        os.mkdir(dir_dest_dir)
    if dir_dest_name == None or dir_dest_name == '':
        # 输入名字默认为当前时间戳
        dir_dest_name = str(int(round(time.time() * 1000)))

    # 遍历目录
    walk = os.walk(dir)
    for parent, dir_names, file_names in walk:
        files = []
        for file in file_names:
            path, ext = os.path.splitext(file)
            if ext.lower() == format:
                files.append((parent + "/" + file))
        merge(files_path=files, dest_dir=dir_dest_dir, dest_name=dir_dest_name)


# 指定多个pdf文档合并
def mergeFiles():
    # 多个文件
    files = None
    files_dest_dir = None
    files_dest_name = None
    # 获取对应的节点信息
    if config.has_section('files'):
        if config.has_option('files', 'files'):
            files = config.get('files', 'files')
        if config.has_option('files', 'dest_dir'):
            files_dest_dir = config.get('files', 'dest_dir')
        if config.has_option('files', 'dest_name'):
            files_dest_name = config.get('files', 'dest_name')
        # 对节点信息进行异常兼容处理
        if files == None or files == '' or files == '[]':
            return
        if files_dest_dir == None or files_dest_dir == '':
            # 默认输出到当前目录
            files_dest_dir = os.path.dirname(__file__)
        if not os.path.exists(files_dest_dir):
            os.mkdir(files_dest_dir)
        if files_dest_name == None or files_dest_name == '':
            # 输入名字默认为当前时间戳
            files_dest_name = str(int(round(time.time() * 1000)))

        # 将files的内容处理处理成数组
        files = files.encode(encoding='utf-8').replace('[', '').replace(']', '').replace(' ', '').split(',')
        merge(files_path=files, dest_dir=files_dest_dir, dest_name=files_dest_name)


# 指定多个文件夹内容所有pdf文档合并
def mergeDirsFiles():
    # 多个目录
    dirs = None
    dirs_dest_dir = None
    dirs_dest_name = None
    # 获取对应的节点信息
    if config.has_section('dirs'):
        if config.has_option('dirs', 'dirs'):
            dirs = config.get('dirs', 'dirs')
        if config.has_option('dirs', 'dest_dir'):
            dirs_dest_dir = config.get('dirs', 'dest_dir')
        if config.has_option('dirs', 'dest_name'):
            dirs_dest_name = config.get('dirs', 'dest_name')
        # 对节点信息进行异常兼容处理
        if dirs == None or dirs == '' or dirs == '[]':
            return
        if dirs_dest_dir == None or dirs_dest_dir == '':
            # 默认输出到当前目录
            dirs_dest_dir = os.path.dirname(__file__)
        if not os.path.exists(dirs_dest_dir):
            os.mkdir(dirs_dest_dir)
        if dirs_dest_name == None or dirs_dest_name == '':
            # 输入名字默认为当前时间戳
            dirs_dest_name = str(int(round(time.time() * 1000)))

        # 遍历目录
        dirs = dirs.encode(encoding='utf-8').replace('[', '').replace(']', '').replace(' ', '').split(',')
        files = []
        for dir in dirs:
            walk = os.walk(dir)
            for parent, dir_names, file_names in walk:
                for file in file_names:
                    path, ext = os.path.splitext(file)
                    if ext.lower() == format:
                        files.append((parent + "/" + file))
        merge(files_path=files, dest_dir=dirs_dest_dir, dest_name=dirs_dest_name)


# 最终都是转化为多个pdf文件的合并
def merge(files_path, dest_dir, dest_name, format='.pdf'):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    merger = PdfFileMerger()
    for file in files_path:
        f = open(file, 'rb')
        merger.append(f)
        f.close()
        print file
    if not dest_dir.endswith('/'):
        dest_dir = dest_dir + '/'
    out_put = open(dest_dir + dest_name + format, 'wb')
    merger.write(out_put)
    merger.close()
    out_put.close()

mergeDirFiles()
mergeFiles()
mergeDirsFiles()
