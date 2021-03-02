# 第二代身份证信息识别
可识别身份证上所有信息：姓名，性别，民族，出生日期，住址，身份证号码。提供Docker镜像部署方式

基于 https://github.com/Raymondhhh90/idcardocr 进行修改

* 使用PaddleOcr进行文字识别，通过接口调用的方式请求本地部署的PaddleOcr服务
* 使用dlib提取身份证图片中的头像，目前根据大致比例提取，有一定白边，有优化空间
* 未处理图片方向，请使用正向图片
* 仅对第二代身份证反面(即带有人像和身份证号码的那一面)有效
* 性别与出生日期不再识别，直接从身份证号码中计算
* 性能还可以继续优化



## 识别率

无生产环境数据，开发测试识别成功率100%，未发现有错误（识别失败、错字）等情况出现



# 开发环境
Win10 + python3.8

## install
> Python依赖安装：<br>
>`sudo pip3 install -r idcardocr/requirements.txt`<br><br>
## 使用方法：
> 本地测试 test.py<br>
> `python3 test.py`<br><br>
> http_server远程接收图片<br>
> `python3 idcard_recognize.py`  <br>
> 默认监听端口为8080 <br><br>
> > 测试:  <br>
> > > 使用curl向服务器发送图片:  <br>
> > > `curl --request POST \
> > > --url http://127.0.0.1:8080 \
> > > --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
> > > --form 'pic=@./testimages/3.jpg'`  <br><br>
> > > 使用Postman：  <br>
> > > ![avatar](postman.jpg) <br>
> > >
> > > 参数mode：
> > >
> > > * 0：只识别身份证号码
> > > * 1：识别身份证上的全部信息
> > > * 2：获取全部信息的同时，还增加头像提取
> >
> > 
> >
> > 


## 性能<br>
> 平台： I5 8259u + 16g macOS 13.14 关闭OpenCL<br>
处理单张图片时间在2.5秒左右（单张图片只能使用单核心）  <br>
~~处理4张图片时间也是4秒左右（4核心）~~  <br>
关于OPENCL: 开启并不会使单张图片处理速度加快，但是能让你在同时间处理更多图片（譬如I5 6500每秒能处理4张图片，开启OPENCL后每秒能处理6张图片） <br> 
开启OPENCL： 默认关闭，可以自行修改`idcard_recognize.http_server`中的`cv2.ocl.setUseOpenCL(False)`开启
