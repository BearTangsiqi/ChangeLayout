#!/usr/bin/env python3
from __future__ import division
import os
import zipfile
import shutil
import string
import re
from xml.parsers.expat import ParserCreate

def Zip(dirname,zipfilename):
    print(r"开始压缩")
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()
    print(r"全部完成")

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
    #压缩
    print(r"压缩成zip包，放在更改的包下，*-new.zip")
    target_file = os.path.splitext(target_name)[0] + r"-new.zip"
    Zip(os.path.splitext(target_name)[0],target_file)
    
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
        global B_FIND
        global FIND_CLASSNAME
        global FIND_PACKAGENAME
        if name == r'favorite':
            if attrs['apkName'] == NEED_APKNAME:
                B_FIND = True
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

def ChangeLayoutXML(apkDirPath,xmlPath,pzXmlPath):
    global NEED_APKNAME
    nameXmlPath = os.getcwd() + r"\name.xml"
    pzXmlPath = os.path.splitext(pzXmlPath)[0] +r"\system\app\Layout.xml"
    pzXml = ''
    f = open(nameXmlPath,'r',encoding='utf-8')
    XML = f.read()
    f.close()
    handler = NameSaxHandler()
    print(r"现有应用为（请勿放入同应用，更新应用请在替换时选择相同的应用）：")
    print(APKLIST1.apkName)
    print(APKLIST2.apkName)
    print(APKLIST3.apkName)
    oneApkPath = ''
    result = ''
    fr = open(xmlPath,'r')
    XMLw = fr.read()
    fr.close()
    answer = input(r"对应用的处理：" + APKLIST1.apkName + r"(y/n)")
    if answer == 'y':
        oneApkPath = input(r"请放入需要替换的apk包(删除请输入a.apk)：")
        NEED_APKNAME = os.path.split(oneApkPath)[1]
        parser = ParserCreate()
        parser.StartElementHandler = handler.start_element
        parser.EndElementHandler = handler.end_element
        parser.CharacterDataHandler = handler.char_data
        parser.Parse(XML)
        if not B_FIND:
            print(r"不是渠道包中的应用，请更新本软件，apk从服务器上下载，勿改名，退出软件")
            exit(0)
        #apk替换,删除本来的apk，再复制添加的apk
        if not APKLIST1.apkName == r"a.apk":
            os.remove(apkDirPath + r"\\" + APKLIST1.apkName)
        if not oneApkPath == r"a.apk":
            shutil.copy(oneApkPath,apkDirPath)
        #布局文件替换，先替换className，再替换packageName
        result,number = re.subn(APKLIST1.className,FIND_CLASSNAME,XMLw)
        result,number = re.subn(APKLIST1.packageName,FIND_PACKAGENAME,result)
        #写入文件布局文件
        fw1 = open(xmlPath,'w')
        fw1.write(result)
        fw1.close()
        #写入文件 配置文件
        fw2 = open(pzXmlPath)
        pzXml = fw2.read()
        pzXml = re.sub(APKLIST1.className,FIND_CLASSNAME,pzXml)
        pzXml = re.sub(APKLIST1.packageName,FIND_PACKAGENAME,pzXml)
        pzXml = re.sub(APKLIST1.apkName,NEED_APKNAME,pzXml)
        fw2.close()
        XMLw = result
        print(r"第一个替换成功")
    #第二个apk
    answer = input(r"对应用的处理：" + APKLIST2.apkName + r"(y/n)")
    if answer == 'y':
        oneApkPath = input(r"请放入需要替换的apk包(删除请输入b.apk)：")
        NEED_APKNAME = os.path.split(oneApkPath)[1]
        parser1 = ParserCreate()
        parser1.StartElementHandler = handler.start_element
        parser1.EndElementHandler = handler.end_element
        parser1.CharacterDataHandler = handler.char_data
        parser1.Parse(XML)
        if not B_FIND:
            print(r"不是渠道包中的应用，请更新本软件，apk从服务器上下载，勿改名，退出软件")
            exit(0)
        #apk替换,删除本来的apk，再复制添加的apk
        if not APKLIST2.apkName == r"b.apk":
            os.remove(apkDirPath + r"\\" + APKLIST2.apkName)
        if not oneApkPath == r"b.apk":
            shutil.copy(oneApkPath,apkDirPath)
        #布局文件替换，先替换className，再替换packageName
        result,number = re.subn(APKLIST2.className,FIND_CLASSNAME,XMLw)
        result,number = re.subn(APKLIST2.packageName,FIND_PACKAGENAME,result)
        #写入文件布局文件
        fw1 = open(xmlPath,'w')
        fw1.write(result)
        fw1.close()
        #写入文件 配置文件
        pzXml = re.sub(APKLIST2.className,FIND_CLASSNAME,pzXml)
        pzXml = re.sub(APKLIST2.packageName,FIND_PACKAGENAME,pzXml)
        pzXml = re.sub(APKLIST2.apkName,NEED_APKNAME,pzXml)
        XMLw = result
        print(r"第二个替换成功")
        #yyy 替换 ads 在第三个字符串中，返回结果字符串和替换次数
        #result,number = re.subn(r"ads", r"yyyyyy", r"asdadskjiohn")
    answer = input(r"对应用的处理：" + APKLIST3.apkName + r"(y/n)")
    if answer == 'y':
        oneApkPath = input(r"请放入需要替换的apk包(删除请输入c.apk)：")
        NEED_APKNAME = os.path.split(oneApkPath)[1]
        parser2 = ParserCreate()
        parser2.StartElementHandler = handler.start_element
        parser2.EndElementHandler = handler.end_element
        parser2.CharacterDataHandler = handler.char_data
        parser2.Parse(XML)
        if not B_FIND:
            print(r"不是渠道包中的应用，请更新本软件，apk从服务器上下载，勿改名，退出软件")
            exit(0)
        #apk替换,删除本来的apk，再复制添加的apk
        if not APKLIST3.apkName == r"c.apk":
            os.remove(apkDirPath + r"\\" + APKLIST3.apkName)
        if not oneApkPath == r"c.apk":
            shutil.copy(oneApkPath,apkDirPath)
        #布局文件替换，先替换className，再替换packageName
        result,number = re.subn(APKLIST3.className,FIND_CLASSNAME,XMLw)
        result,number = re.subn(APKLIST3.packageName,FIND_PACKAGENAME,result)
        #写入文件布局文件
        fw1 = open(xmlPath,'w')
        fw1.write(result)
        fw1.close()
        #写入文件 配置文件
        pzXml = re.sub(APKLIST3.className,FIND_CLASSNAME,pzXml)
        pzXml = re.sub(APKLIST3.packageName,FIND_PACKAGENAME,pzXml)
        pzXml = re.sub(APKLIST3.apkName,NEED_APKNAME,pzXml)
        XMLw = result
        print(r"第三个个替换成功")
    fw3 = open(pzXmlPath,'w')
    fw3.write(pzXml)
    fw3.close()

def ChangeAPKList(target_dir,target_name):
    layoutPath = os.path.splitext(target_name)[0] + APKPATH
    layoutChangeFilePath = os.path.splitext(target_name)[0] + APKLAYOUT
    print(r"apk存放的位置为：" + layoutPath)
    if LAYOUTTYPE == 'xml':
        print("xml TYPE")
        ChangeLayoutXML(layoutPath,layoutChangeFilePath,target_name)
    elif LAYOUTTYPE == 'db':
        print("db TYPE")
    elif LAYOUTTYPE == 'apk':
        print("此ROM需要反编译才能更改布局，只能更换应用")
    else:
        print("此ROM未经过处理，退出")
        exit(0)

def main():
    print(r"注意：只能对三个应用更换")
    Unzip(os.getcwd())

if __name__=='__main__':
    main()
