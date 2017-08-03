# -*- coding:utf-8 -*-
import requests
import r18htmlPyParse






urlLink = 'https://r18cn.com/page/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }

class r18URLRequestManager(object):




    def __init__(self):

        #新的爬虫网址
        self.newURLs = set()
        #旧的爬虫网址
        self.oldURLs = set()

        self.currentPage = 1
        #最大主页爬虫深度
        self.maxMainPageClawDepth = 1


    #添加单一元组
    def addNewURL(self,url):
        if url is None:
            return

        if self.currentPage < self.maxMainPageClawDepth :
            return

        #添加进爬虫列表网址
        if url not in self.newURLs and url not in self.oldURLs:
            self.newURLs.add(url)

    #添加数组元组
    def addNewURLs(self,urls):

        if len(urls) == 0:
            return
        for url in urls:
            if url not in self.newURLs and url not in self.oldURLs:
                self.newURLs.add(url)



    def hasNewURL(self):
        return len(self.newURLs) != 0



    def getNewURL(self):
        new_url = self.newURLs.pop()
        self.oldURLs.add(new_url)
        return new_url



    def startRequest(self,url):
        #传入的url是个元组，一个是网址，第二个是type


        if url[1] == "MainPage":
            #最大的主页爬虫深度
            if int(self.currentPage) > int(self.maxMainPageClawDepth):
                print('超过最大爬虫页数')
                return

            print("Start Request Main Page Count %s=======>" %(self.currentPage))


        try:

            r = requests.get(url=url[0], headers = headers , timeout = 5.0)

        except Exception as e:

            print('无法读取网页')
            print(e)
            if url[1] == "MainPage":
                print("End Request Main Page %s Count =======>" %self.currentPage)
            else:
                print("subPage : %s Fail to Load !"%url[0])
            return



        if url[1] == "MainPage":
            self.currentPage += 1

        print('End Request url =====>%s'%(url[0]))

        # print(r.text)

        return (r.text,url[1])









