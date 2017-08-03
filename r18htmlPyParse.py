# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import bs4
import requests

pageNotToClaw = 'https://r18cn.com'

class r18htmlPyParseManger(object):

    #传入的是HtmlString
    def __init__(self ):
        pass




    #分析主Page页的方法
    def beginAnalyzeMainPage(self,htmlString):

        infomationReq = []

        if htmlString is not None:



            soup = BeautifulSoup(htmlString[0], 'html.parser' )


            #获得本页所有影片信息
            container = soup.find_all('li',class_="post box row fixed-hight")

            for containers in container:
                #获得每部影片下个地址
                containers = containers.find_all('a',class_="zoom")

                for infoLink in containers:

                    #获取每个子页的消息
                    infomationReq.append((infoLink['href'],"SubPage"))


            #获取当前主页的页数
            # pageContainer = soup.find_all('a',class_ = "current")
            # infomationReq.append((infoLink['href'],"MainPage"))

            pageContainer = soup.find_all('div', class_="navigation container")
            for pageContainers in pageContainer:
                pageLink = pageContainers.find_all('a')
                for pageLinks in pageLink:
                    #防止再爬一次首页
                    if pageLinks['href'] != pageNotToClaw:
                        infomationReq.append((pageLinks['href'],"MainPage"))


            # print(pageContainer)

        return infomationReq


    #传入元组数据，数据格式同上
    def beginAnalyzeSubPage(self,htmlString):
        if htmlString is not None:
            soup = BeautifulSoup(htmlString[0], 'html.parser')

            # print(soup.p)



            #Publish Date
            # print(soup.find_all('span', class_ ='info_date info_ico'))
            publishDate = (soup.find('span', class_ ='info_date info_ico')).get_text()

            #info
            videoInfoNode = soup.find('div', id = 'post_content')
            # print(videoInfoNode.get_text())
            # print(videoInfoNode)
            videoInfo = videoInfoNode.get_text()



            #cover
            cover = ''
            for _ in videoInfoNode.p.contents:

                #区分type类型
                if type(_)  == bs4.element.NavigableString:
                    pass
                else:
                    try:
                        if(len(_.contents)) == 0:
                            #直接获取src
                            # print(_['src'])
                            print(_)
                            cover = _['src']
                        else:
                            #还有一个节点
                            for __ in _.contents:
                                # print(__['src'])

                                cover = __['src']
                    except Exception as e:
                        print("图片无法获取===> 百度图片替代")

                        cover = 'https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white_fe6da1ec.png'

            #picInfo



            #Title Name
            _ = soup.find_all('div' , class_ = 'article_container row box' )
            titleName = ''
            for __ in _:

                titleName = __.find('h1').get_text()
                if titleName:
                    break
            newList = [titleName,publishDate,videoInfo,cover]
            return newList

