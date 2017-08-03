# pyR18 Clawer
## r18.cn 你懂的内容爬取(仅供学习)



### 注意:
* Python3 环境
* 需要 Requests ， Beautifulsoup4  库

### 使用方法:
1. 修改文件夹中 emailList.txt ， 添加需要发送到的邮箱，支持连发
2. 修改 r18EmailModule.py 中发邮件所需信息
3. 可修改pyMain.py中爬虫深度，默认2页
4. 可修改读取数据库数量，默认传入当天日期，如果有更新自动会发送(服务器自动部署计划)


```python
#运行
python pyMain.py
```

流程：
1.     先从根网址请求网址,请求到的Html 筛选出 MainPage 和 SubPage
2.     根据Main和Sub不同再解析
3.     Sub中的图片信息下载和存档
4.     生成Html，压缩，发送

