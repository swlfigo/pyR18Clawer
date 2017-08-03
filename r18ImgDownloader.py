# -*- coding:utf-8 -*-
import os
import requests
import uuid

class ImgDownloader(object):
    def __init__(self):
        self.currentPath = os.path.dirname(os.path.abspath("__file__"))
        self.currentPath = os.path.join(self.currentPath, 'imageManger')
        if os.path.exists(self.currentPath) == False:
            print('文件夹不存在==>创建文件夹:%s'%self.currentPath)
            os.mkdir(self.currentPath)
        else:
            print('存在存放文件夹')

    def isExistsFilePath(self, filePath):
        if os.path.exists(filePath) == False:
            return False
        else:
            return True


    def startDownloadImg(self,videoInfoList):
        if videoInfoList and videoInfoList[3] is not None:

            try:

                ir = requests.get(videoInfoList[3])

            except Exception as e:

                print('DownLoadImgFail  ====> 使用默认图片替代')

                filePath = '/default.png'

                videoInfoList.append(filePath)

                return videoInfoList

            if ir.status_code == 200:
                #下载成功
                fileName = uuid.uuid4()
                filePath = os.path.join(self.currentPath,str(fileName) + '.jpg')
                videoInfoList.append(filePath)
                if self.isExistsFilePath(filePath) == True:
                    return videoInfoList

                #写入本地
                with open(filePath,'wb') as f:
                    f.write(ir.content)

                print('writeFinish')
                f.close()

                return videoInfoList