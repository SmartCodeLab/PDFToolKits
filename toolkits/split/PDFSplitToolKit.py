# -*- coding:utf-8 -*-
import os
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter

try:
    import configparser
except ImportError:
    import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

configFile = os.path.dirname(__file__) + '/android01.config'

try:
    config = configparser.ConfigParser()
except Exception as e:
    config = ConfigParser.ConfigParser()

config.read(configFile, encoding='utf-8')

# 获取配置信息
bookTitle = config.get('book', 'title')
print bookTitle
bookPath = config.get('book', 'path')
print bookPath
out_put_dir = config.get('book', 'output_dir')
start = config.get('book', 'start').encode(encoding='utf-8')
start = start.replace('[', '').replace(']', '').replace(' ', '').split(',')
print start
end = config.get('book', 'end').encode(encoding='utf-8')
end = end.replace('[', '').replace(']', '').replace(' ', '').split(',')
print end
chapter = config.get('book', 'chapter').encode(encoding='utf-8')
chapter = chapter.replace('[', '').replace(']', '').replace(' ', '').replace('\n','').split(',')
print chapter[0]

pdf_file = PdfFileReader(open(bookPath), "rb")
pad_pages_number = pdf_file.getNumPages()

# 创建输出目录
dir = os.path.dirname(__file__) + "/" + out_put_dir + "/"
if not os.path.exists(dir):
    os.mkdir(dir)

# 分割PDF
for index in range(len(chapter)):
    out_put = PdfFileWriter()
    for page in range(int(start[index]), int(end[index])):
        out_put.addPage(pdf_file.getPage(page))
    out_put_stream = open(dir + bookTitle + "(" + str(chapter[index]) + ").pdf", "wb")
    out_put.write(out_put_stream)
