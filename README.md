![:name](https://count.getloli.com/get/@muzi-xiaoren-kaobei_Crawler?theme=gelbooru)

# kaobei_Crawler
主要使用selenium库模拟浏览器来获取kaobei动态加载的html页面。

用BeautifulSoup进行解析。然后传入函数先获取url。

将url传入get.py中使用多线程编程加快下载速率

拷贝主页为<https://www.mangacopy.com/>

下面是具体函数及使用方法。

download.py 和 get.py 是一般不需要修改。pic是md图片存放处。

---

## kaobei_spider_1.py

最开始输入

0->全部下载在同一文件夹内

1->分文件夹进行下载

下图前面的文件夹是1的效果，在外面的图片是0的效果
![](src/img_1.png)

使用临时账号和密码登陆，需要登陆的原因是有一些漫画不登陆不可见
(在52和53行处,可以不用修改 也可以修改成你的账号和密码)

### 在59行处修改漫画页面的url，修改成页面显示如下图时的url。从浏览器复制就行。
![](src/img.png)

下载的图片新存放于本文件夹中的新建获取网页漫画名的文件夹中。

---

## kaobei_spider_2.py

~~### 在41行处修改漫画页面的url~~

~~使用的是本机浏览器，例如代码中的Chrome浏览器,如果你的浏览器中已经登陆了拷贝网站，那么就可以省去登陆的步骤。~~

~~但是配置起来比较麻烦(不推荐使用,后续更新也暂不考虑此处)，教程见[教程](https://blog.csdn.net/beckynie1989/article/details/124262163)<https://blog.csdn.net/beckynie1989/article/details/124262163>~~

~~使用前需要关闭所有浏览器页面    然后打开终端输入    Chrome --remote-debugging-port=9222~~

~~建议直接使用kaobei_spider_1的账号密码登陆~~

此文件不再更新维护，仅供参考。

---

## 最后是一些注意事项
1. 可能需要开梯子才能正确下载，我换了梯子后可以完美正常下载，不开梯子会有报错。和拷贝服务器在外有关系吧。


2. 大量下载困会导致部分漫画连接错误，可以多运行程序几次，重复图片不会再次下载，可以补全之前连接错误没能下载的图片。


3. 程序运行时请让浏览器的页面保持在屏幕中，不要最小化到任务栏中，不然页面可能不会进行更新。


4. 文件名格式由章节数_图片顺序_url中部分字符串构成。如下所示。
![](src/img1.png)

5. 因为每章漫画的页数不同，所以为了便于下载。可以提前修改count的值(kaober_Crawler_1第74行) 


    页数<60时，使用默认值count=4 

    页数60<i<120 ，可修改count=8

    页数>200，可修改count=16





