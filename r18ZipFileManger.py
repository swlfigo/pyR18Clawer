# -*- coding:utf-8 -*-
import zipfile
import os
import shutil

class zipFileManger:

    def __init__(self):
        pass


    def zipFileWithPath(self, dirName , zipFileName ):

        """
            | ##@函数目的: 压缩指定目录为zip文件
            | ##@参数说明：dirname为指定的目录，zipfilename为压缩后的zip文件路径
            | ##@返回值：无
            | ##@函数逻辑：
        """


        if dirName is None:
            return
        if zipFileName is None:
            return

        zipName = zipFileName

        filelist = []
        if os.path.isfile(dirName):
            filelist.append(dirName)
        else:
            for root, dirs, files in os.walk(dirName):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipName, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirName):]
            zf.write(tar, arcname)
        zf.close()






    def unzip_file(self, zipfilename , unziptodir):
        """
        | ##@函数目的: 解压zip文件到指定目录
        | ##@参数说明：zipfilename为zip文件路径，unziptodir为解压文件后的文件目录
        | ##@返回值：无
        | ##@函数逻辑：
        """
        if not os.path.exists(unziptodir):
            os.mkdir(unziptodir, 0o0777)
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\', '/')

            if name.endswith('/'):
                p = os.path.join(unziptodir, name[:-1])
                if os.path.exists(p):
                    # 如果文件夹存在，就删除之：避免有新更新无法复制
                    shutil.rmtree(p)
                os.mkdir(p)
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir = os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir):
                    os.mkdir(ext_dir, 0o0777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
