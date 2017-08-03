# -*- coding:utf-8 -*-
import r18DBManager
import datetime
import os
import shutil
import r18ZipFileManger
import r18EmailModule

class imOutputer(object):

    infoMarkDown = []

    infoHtml = []

    def __init__(self):

        self.dbManger = r18DBManager.VMDBMangaer()
        self.zipManager = r18ZipFileManger.zipFileManger()
        self.emailManger = r18EmailModule.r18EmailModule()

    def isExistsFilePath(self, filePath):
        if os.path.exists(filePath) == False:
            return False
        else:
            return True

    #从文件夹提取图片
    def startTransformDate(self,date = None):

        transDate = ''
        if date is None:

            now = datetime.datetime.now()

            transDate = now.strftime('%Y-%m-%d')
        else:
            transDate = date



        self.date = transDate
        self.transPath = os.path.dirname(os.path.abspath("__file__"))
        self.transPath = os.path.join(self.transPath, transDate)

        if self.isExistsFilePath(self.transPath):
            shutil.rmtree(self.transPath)

        #创建文件夹
        os.mkdir(self.transPath)
        imgResourceFile = os.path.join(self.transPath, 'imgResourceFile')
        # print(imgResourceFile)
        if self.isExistsFilePath(imgResourceFile):
            pass
        else:
            os.mkdir(imgResourceFile)



        #读取数据库

        if transDate == 'ALL':
            sqlString = ''' SELECT * FROM r18InfoTable'''
        else:
            sqlString = ''' SELECT * FROM r18InfoTable where publishDate = '%s' '''%transDate


        self.result = self.dbManger.execute(sqlString)
        print('数据库查询长度%d',len(self.result))
        if len(self.result) == 0:
            return False

        self.imageResource = []
        #将资源图片移动到TransPath
        for index in range(len(self.result)):
            if self.isExistsFilePath(self.result[index][2]):
                #返回是移动后文件路径
                path = shutil.copy(self.result[index][2],imgResourceFile)

                os.rename(path,imgResourceFile + os.sep + str(index) + '.jpg')
                newPath = os.path.join('imgResourceFile', str(index) + '.jpg')
                self.imageResource.append(newPath)





    #生成MarkDown
    def generateMarkDown(self):
        if len(self.result) == 0 :
            return

        markDownString = ''

        markDownString = '# ' + self.date + '影片更新 \n'
        for index in range(len(self.result)):
            markDownString = markDownString + '#### ' + str(self.result[index][1]) + '\n'
            markDownString = markDownString + '![](%s) \n' %self.imageResource[index]
            markDownString = markDownString + str(self.result[index][5]) + '\n\n\n'


        filePath = os.path.join(self.transPath, '今日更新' + '.md')
        if self.isExistsFilePath(filePath):
            os.remove(filePath)

        with open(filePath,'wb') as f:
            f.write(markDownString.encode('utf-8'))

        f.close()

    #生成html
    def generateHTML(self):
        if len(self.result) == 0 :
            return
        htmlString = '''
<head>
<title>今日更新</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<html>
<body>
<h1>%s</h1>
        '''%self.date
        htmlString = htmlString + '<p>'

        print('Result长度 :%d'%(len(self.result)))
        print('Resource长度%d'%(len(self.imageResource)))

        for index in range(len(self.result)):

            try:
                htmlString = htmlString + '<h3>%s</h3>'%self.result[index][1] + '\n'
                htmlString = htmlString + '''<img src = '%s'>'''%self.imageResource[index] + '\n'

                string = (self.result[index][5]).replace('\n' , '</br>')


                htmlString = htmlString + '<p>%s</p>'%string + '\n'
            except Exception as e:
                print(e)
                print('生成当前项失败 index%d'%index)
                continue

        htmlString = htmlString + '</p>\n</body>\n</html>'
        filePath = os.path.join(self.transPath, '今日更新' + '.html')
        if self.isExistsFilePath(filePath):
            os.remove(filePath)

        message = """
        <html>
        <head></head>
        <body>
        <p>Follow two parameters</p>
        <p>1</p>
        <p>2</p>
        </body>
        </html>"""

        with open(filePath, 'w') as f:
            f.write(htmlString)

        f.close()


    def zipFileResource(self):
        self.zipPath = os.path.dirname(os.path.abspath("__file__"))
        self.zipPath = os.path.join(self.zipPath, self.date + '.zip' )
        self.zipManager.zipFileWithPath(self.transPath,self.zipPath)


    def sendEmail(self):
        self.emailManger.fileContent.append(self.zipPath)
        self.emailManger.startSendEmail()


    #清除数据
    def clean(self):
        if self.isExistsFilePath(self.transPath):
            shutil.rmtree(self.transPath)
        if self.isExistsFilePath(self.zipPath):
            os.remove(self.zipPath)
        self.imgPath = os.path.dirname(os.path.abspath("__file__"))
        self.imgPath = os.path.join(self.imgPath, 'imageManger')
        if self.isExistsFilePath(self.imgPath):
            shutil.rmtree(self.imgPath)