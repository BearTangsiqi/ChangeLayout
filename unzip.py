#!/usr/bin/env python3
from __future__ import division
import os
import zipfile
import shutil
import string
import re
from xml.parsers.expat import ParserCreate

def Zip(target_dir):
	target_file=os.path.basename(os.getcwd())+'.zip'
	zip_opt=input("Will you zip all the files in this dir?(Choose 'n' you should add files by hand)y/n: ")
	while True:
		if zip_opt=='y':       #compress all the files in this dir
			filenames=os.listdir(os.getcwd())    #get the file-list of this dir
			zipfiles=zipfile.ZipFile(os.path.join(target_dir,target_file),'w',compression=zipfile.ZIP_DEFLATED)
			for files in filenames:
				zipfiles.write(files)
			zipfiles.close()
			print("Zip finished!")
			break
		elif zip_opt=='n':     #compress part of files of this dir
			filenames=list(input("Please input the files' name you wanna zip:"))
			zipfiles=zipfile.ZipFile(os.path.join(target_dir,target_file),'w',compression=zipfile.ZIP_DEFLATED)
			for files in filenames:
				zipfiles.write(files)
			zipfiles.close()
			print("Zip finished!")
			break
		else:
			print("Please in put the character 'y' or 'n'")
			zip_opt=input("Will you zip all the files in this dir?(Choose 'n' you should add files by hand)y/n: ")

def Unzip(target_dir):
    target_name=input("请放入zip包：")
    print("正在解压，请稍等。。。")
    #删除可能不重复的文件
    if os.path.exists(os.path.splitext(target_name)[0]):
        shutil.rmtree(os.path.splitext(target_name)[0])
    zipfiles=zipfile.ZipFile(target_name,'r')
    zipfiles.extractall(os.path.splitext(target_name)[0])
    zipfiles.close()
    print(r"解压完毕，读取信息中。。。")
    ReadInformation(target_dir,target_name)

class ApkInfomation(object):
    __slots__ = ('packageName','className','apkName')

APKPATH = ''
LAYOUTTYPE = ''
APKLIST1 = ApkInfomation()
APKLIST2 = ApkInfomation()
APKLIST3 = ApkInfomation()
APKLAYOUT = ''
COUNTAPK = 0

class LayoutSaxHandler(object):
    def start_element(self, name, attrs):
        #print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))
        global COUNTAPK
        if name == 'apkPath':
            global APKPATH
            global LAYOUTTYPE
            APKPATH = str(attrs['apkPath'])
            LAYOUTTYPE = str(attrs['layoutType'])
        elif name == 'apkList1':
            global APKLIST1
            APKLIST1.packageName = str(attrs['packageName'])
            APKLIST1.className = str(attrs['className'])
            APKLIST1.apkName = str(attrs['apkName'])
            COUNTAPK = 1
        elif name == 'apkList2':
            global APKLIST2
            APKLIST2.packageName = str(attrs['packageName'])
            APKLIST2.className = str(attrs['className'])
            APKLIST2.apkName = str(attrs['apkName'])
            COUNTAPK = 2
        elif name == 'apkList3':
            global APKLIST3
            APKLIST3.packageName = str(attrs['packageName'])
            APKLIST3.className = str(attrs['className'])
            APKLIST3.apkName = str(attrs['apkName'])
            COUNTAPK = 3
        elif name == 'apkLayout':
            global APKLAYOUT
            APKLAYOUT = str(attrs['FilePath'])

    def end_element(self, name):
        #print('sax:end_element: %s' % name)
        pass

    def char_data(self, text):
        #print('sax:char_data: %s' % text)
        pass

B_FIND = False
FIND_PACKAGENAME = ''
FIND_CLASSNAME = ''
NEED_APKNAME = ''
class NameSaxHandler(object):
    def start_element(self, name, attrs):
        #print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))
        if attrs['apkName'] == NEED_APKNAME:
            global B_FIND
            B_FIND = TRUE
            FIND_CLASSNAME = attrs['className']
            FIND_PACKAGENAME = attrs['packageName']
    def end_element(self, name):
        pass

    def char_data(self, text):
        pass
        
def ReadInformation(target_dir,target_name):
    layoutPath = os.path.splitext(target_name)[0] +r"\system\app\Layout"
    if os.path.isfile(layoutPath):
        print(r"此包未做过处理，请联系适配组")
        exit(0)
    LayoutPath2 = layoutPath + r'.xml'
    f = open(LayoutPath2,'r')
    InformationXML = f.read()
    f.close()
    handler = LayoutSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(InformationXML)
    print(r"信息读取完毕")
    ChangeAPKList(target_dir,target_name)

def ChangeLayoutXML(apkDirPath,xmlPath):
    print(apkDirPath)
    print(xmlPath)
    nameXmlPath = os.getcwd() + r"\name.xml"
    print(nameXmlPath)
    answer = input(r"是否替换应用：" + APKLIST1.apkName + r"(y/n)")
    oneApkPath = ''
    if answer == 'y':
        oneApkPath = input(r"请放入需要替换的apk包：")
        #yyy 替换 ads 在第三个字符串中，返回结果字符串和替换次数
        #result,number = re.subn(r"ads", r"yyy", r"asdadskjiohn")
        

def ChangeAPKList(target_dir,target_name):
    layoutPath = os.path.splitext(target_name)[0] + APKPATH
    layoutChangeFilePath = os.path.splitext(target_name)[0] + APKLAYOUT
    print(r"apk存放的位置为：" + layoutPath)
    if LAYOUTTYPE == 'NULL':
        pass
    elif LAYOUTTYPE == 'xml':
        print("xml TYPE")
        ChangeLayoutXML(layoutPath,layoutChangeFilePath)
    elif LAYOUTTYPE == 'db':
        print("db TYPE")
    elif LAYOUTTYPE == 'apk':
        print("此ROM需要反编译才能更改布局，只能更换应用")

def main():
    Unzip(os.getcwd())

if __name__=='__main__':
    main()
