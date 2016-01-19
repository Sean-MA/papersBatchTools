#! /usr/bin/env python3
#coding:utf-8

import urllib.request
import urllib.parse
import ssl
import os
from bs4 import BeautifulSoup

print ("papersBatchTools v0.1")
numFailed2Download = 0
numDownloaded = 0
ssl._create_default_https_context = ssl._create_unverified_context

with open('keyWords.txt', 'r') as f:
	read_data = '0'
	print("Input the number of papers need to be downleaded: ")
	paperNumStr = input()
	keyWords = {}
	keyWords2Encode = {}
	while read_data != '':
		read_data = f.readline().strip('\n')
		pageNum = 0
		paperNum = int(paperNumStr)
		if read_data != '':
			os.mkdir(read_data)
			print("make dir: " + read_data)
			os.chdir(read_data)
			print("change to dir: " + read_data)
			while paperNum != 0:
				keyWords[read_data]=read_data
				keyWords2Encode['kewWords2Encode']=keyWords[read_data]
				url_values=urllib.parse.urlencode(keyWords2Encode)
				print(read_data +' ' + keyWords[read_data] + ' ' + url_values)
				url = "https://scholar.google.com.tw/scholar?start="
				url1 = "lr=&q="
				url2 = "&hl=en&as_sdt=0,5"

				webURL = url + str(pageNum) + url1 + url_values[16:] + url2
				print(webURL)
				hdr = { 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
	       				'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	        			'Accept-Language': "en-US,en;q=0.5",
	       				'Connection': "keep-alive"}
				req = urllib.request.Request(webURL, headers = hdr)
				webPage = urllib.request.urlopen(req).read()
				webPage = webPage.decode('gbk', 'ignore').encode('utf-8')
				webPage = webPage.decode('utf-8')
				soup = BeautifulSoup(webPage, 'html.parser')
				print("\n")
				for paper in soup.find_all("div", class_="gs_md_wp gs_ttss"):
					for child in paper.children:
						if paperNum <= 0:
		   					break
						else:
			   				print(child.get('href'))
			   				try:
			   					downloadsFile = urllib.request.Request(child.get('href'), headers = hdr)
			   					paperFile = urllib.request.urlopen(downloadsFile, timeout = 80).read()
			   				except urllib.error.URLError as e:
			   					print(e.reason)
			   					numFailed2Download = numFailed2Download + 1
			   					pass
			   				for hs in child.parent.parent.parent.find("div", class_="gs_ri").children:
			   					fileName = hs.get_text()
			   					print("paper title: " + fileName)
			   					fileName = fileName.replace(':','')
			   					fileName = fileName.replace('"','')
			   					fileName = fileName.replace("'",'')
			   					fileName = fileName.replace(' ','')
			   					fileName = fileName.replace('-','')
			   					fileName = fileName.replace('/','')
			   					fileName = fileName.replace('\\','')
			   					fileName = fileName.replace('?','')
			   					print("fileName: " + fileName)
			   					with open(fileName + ".pdf","wb") as code:
			   						code.write(paperFile)
			   					paperNum = paperNum - 1	
			   					print("!!!! paper num :" + str(paperNum))
			   					numDownloaded = numDownloaded + 1	   					
			   					break
				if paperNum <= 0:
					print("switch back")
					os.chdir("..")
					break
				else:
		   			pageNum = pageNum + 10;


print(str(numFailed2Download) + "file(s) failed to download... " + str(numDownloaded) + "files(s) downloaded...")
