# -----
Python 大麦网自动抢票-德云社自动抢票

大麦网演唱会抢票程序---参考自github 作者：MakiNaruto  地址：https://github.com/MakiNaruto/Automatic_ticket_purchase[1]
## 安装环境
* Python3.6
* Selenium
* chrome浏览器，需要下载ChromeDriver包及配置  http://chromedriver.storage.googleapis.com/index.html 
````
通过 cookie 保存登录信息，可以实现全自动刷新。
此代码主要是根据德云社购票窗口连接编写，主要实现选座后的全自动实现
需要购买其他票可以基于此改编
抢票速度基于网速，实测 3s
````

###strat 
* 1|安装必要环境
* 2|复制抢票网址到抢票目标页，运行 damai_dys_master.py
* 3|扫码登录后即可自动刷新，抢票
* 4|对于德云社界面需要选座，在进入选座界面后需要自己点击想选择的座位，然后无需任何操作就可以完成抢票。***
* 5|此代码目前不可以实现日期和场次的选择，会自动选择第一个。！！！（待完善……）

最后成功测试运行时间：2019-12-20。此方法太过于依赖页面源码的元素ID、xpath、class,若相应的绝对路径寻找不到会出现问题。
建议自己先测试一遍，自行定位相应的绝对路径或用更好的定位方法替代。[1]
