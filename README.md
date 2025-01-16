**一、应用介绍**\
本应用为基于WebGIS的校园共享单车调度系统。

**注意**：此应用并不是完整版，因为涉及到高德地图的密匙问题、数据库的构建和最优数量矩阵的构建等问题，因此不能够上手直接运行，请自行更该相应位置后再进行运行。

**二、所用工具**\
1.程序所用框架：本应用前端所使用的是高德Api作为地图服务，前端框架为Vue，后端框架为Django，数据库为PostgreSQL及扩展PostGIS。

2.程序所调用库：\
前端：\
Ant Design：主要作用是对页面的设计。

HTTP请求库:\
Axios：用以发送请求。

后端:\
Django REST framework: 一个强大的和灵活的工具包，用于构建 Web API。\
django.contrib.gis: Django 的地理信息系统（GIS）扩展，用于处理地理数据。\
django-cors-headers: 用于处理跨源资源共享（CORS）的中间件。\
djangorestframework-simplejwt: 提供 JSON Web Token（JWT）认证支持的 Django REST framework 扩展。\
djangorestframework-gis: Django REST framework 的 GIS 扩展，用于处理地理数据的序列化和反序列化。\
Pandas: 一个强大的数据分析和操作库，用于处理表格数据。\
Heapyq: Python 标准库中的一个模块，提供了堆队列算法，也称为优先队列算法。\
GDAL: 一个用于读写栅格和矢量地理空间数据的库，通过 GDAL_LIBRARY_PATH 配置在 Django 中使用。

**三、具体功能**\
1.框架页面：主要显示标题、logo、各个功能页面的索引、登入页面和注册按钮。

2.首页：首页采取Ant Design的Carousel（走马灯）控件，对基础本的功能进行滚动式播放。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/9.jpg)

3.登入界面：登入界面嵌入到了框架页面，以弹窗的形式展示。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/10.jpg)

4.注册页面：通过登入弹窗的右下角按钮进入注册页面，注册成功后立马返回主页。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/11.jpg)

5.车量情况统计：可以通过下拉框选择不同的条件进行查询。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/3.jpg)

6.车辆位置总览：该模块将车辆位置展示出来，并给出一些基础功能。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/4.jpg)
![iamge](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/2.jpg)

7.车辆位置调度：该模块通过已知的最优数量矩阵和现有数量矩阵求差，得到调度数量矩阵，通过条件带入Dijkstra算法里，返回调度数据。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/5.jpg)
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/6.jpg)

8.火灾预警：该模块通过选择指定id的车辆分别在前端以该点生成50m和100m的圆，在后端会对事故车进行缓冲区分析，将50m范围内的车抛给前端，对这些车用红色图标进行覆盖。
![image](https://github.com/sulangren/webGIS--GaodeApi-tramDispatch/blob/master/image/7.jpg)

**四、补充**\
如果想要直接使用的话，请记得收藏该项目，并表明出处，谢谢。\
作者近段时间比较忙，需要帮助文档的话，请等待一段事件，等作者处理完后会更新文档，并发布帮助文档。
