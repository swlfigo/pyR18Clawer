# -*- coding:utf-8 -*-
import r18URLRequest
import r18htmlPyParse
import r18DBManager
import r18ImgDownloader
import r18InfomationOutputer
import time


class MainClaw(object):

    def __init__(self):
        self.urlManger = r18URLRequest.r18URLRequestManager()
        self.htmlParser = r18htmlPyParse.r18htmlPyParseManger()
        self.dbManger = r18DBManager.VMDBMangaer()
        self.imgDownloader = r18ImgDownloader.ImgDownloader()
        self.outputer = r18InfomationOutputer.imOutputer()



    def starClaw(self,root_url):
        #通过元组存储数据, 第一个是url，第二个是type
        self.urlManger.addNewURL((root_url,'MainPage'))
        self.urlManger.maxMainPageClawDepth = 2
        while self.urlManger.hasNewURL():
            #若存在新链接
            new_url = self.urlManger.getNewURL()
            #返回一个元组
            htmlContent = self.urlManger.startRequest(new_url)
            if htmlContent is not None:
                if htmlContent[1] == "MainPage":
                    # 主页的Html内容
                    urlInfo = self.htmlParser.beginAnalyzeMainPage(htmlContent)
                    self.urlManger.addNewURLs(urlInfo)

                elif htmlContent[1] == "SubPage":
                    #副页的Html内容
                    # print(htmlContent[0])
                    # print(new_url[0])
                    #titleName, publishDate, videoInfo, cover

                    videoInfoList = self.htmlParser.beginAnalyzeSubPage(htmlContent)
                    #下载Cover
                    #最后一个键值是本地路径
                    videoInfoListNew = self.imgDownloader.startDownloadImg(videoInfoList)
                    if videoInfoListNew == False:
                        continue
                    #入库
                    self.dbManger.startRecord(videoInfoListNew)

        # 生成MarkDown or Html
        date = str((time.localtime())[0] + '-' + (time.localtime())[1]  +  '-'  + (time.localtime())[2]  )
        flag = self.outputer.startTransformDate(date)
        if flag == False:
            return
        self.outputer.generateHTML()


        # Zip
        self.outputer.zipFileResource()

        #Send Email
        self.outputer.sendEmail()


        # clean
        self.outputer.clean()


if __name__ == '__main__':


    rootURL = urlLink = 'https://r18cn.com/page/1'
    objSpiderClaw = MainClaw()
    objSpiderClaw.starClaw(rootURL)


