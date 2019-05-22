# yxSpider

## 环境
1. 框架：scrapy
2. 第三方库：selenium, requests, fake-useragent, re, Pillow
3. 将 YDMHTTPDemo.py 文件中的用名户和密码 填写云打码账号。

## 运行
1. 启动代理ip 需要配置 redis数据库，如本地已有redis数据库可跳过以下步骤
   > cmd 进入 proxy文件夹中的redis文件中，输入 redis-server.exe redis.windows.conf 启动redis数据库即可。\n
   > \n在运行 步骤 2 即可，
2. proxy 文件中的ProxyPool-master为代理ip，启动该文件下的 run.py 即可。
3. 运行 YXSpider文件中debug.py 文件即可运行程序 （需配置 YDMHTTPDemo.py 文件中的用名户和密码）
