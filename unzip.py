#!/usr/bin/env python3
import os
import zipfile
import shutil

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
	
def ReadInformation(target_dir,target_name):
	layout = os.path.splitext(target_name)[0] +r"\system\app\Layout.xml"
	print(layout)

def main():
	Unzip(os.getcwd())
	
	
if __name__=='__main__':
	main()
