# Camera Basic 单相机标定
## 功能说明
该程序通过相机拍摄的棋盘格图片进行相机标定，获得相机内参、畸变系数以及每张图片对应的旋转向量、位移向量。
## 代码文件夹结构
```
cameraBasic
│  calImpZhang.py    		#张友正标定的实现
│  cemeraBasicMain.py		#主程序，包括opencv和自己写的张友正标定的运行
│  README.md
│  __init__.py
│
├─compare				#自己实现的张友正标定和openCV的结果比较
│  ├─opencv				#以下是openCV的标定结果
│  │      cameraMatirx.txt	#相机内参矩阵（3*3）
│  │      mdisCoeffs.txt	#相机畸变系数 (k1,k2,k3,p1,p2)
│  │      rvecs.txt		#各个图片的旋转向量
│  │      tvecs.txt		#各个图片的位移向量
│  │
│  └─zhang
│          cameraMatirx.txt	#以下是openCV的标定结果
│          mdisCoeffs.txt	#相机内参矩阵（3*3）
│          rvecs.txt		#相机畸变系数 (k1,k2,0,0,0)
│          tvecs.txt		#各个图片的位移向量
│
├─img				#图片文件夹
│  ├─left			#左侧相机拍摄图像
│  │      left01.jpg
│  │      left02.jpg
│  │      ......
│  │      left14.jpg
│  │
│  └─right
│          right01.jpg
│          right02.jpg
│          ......
│          right14.jpg
│
└─__pycache__
```
## 程序使用方法
1. 直接运行`cemeraBasicMain`，弹出选择文件夹框，如图所示
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/selectFloder.jpg)
2. 选择文件夹后，命令行输入棋盘格size：
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/inputBoardsize.jpg)
3. 程序会自动运行openCV的API实现的标定以及我自己实现的张友正标定
4. 运行中会弹出每张图片原图和去畸变之后的图像，按任意键切换到下一张图像
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/undisort.jpg)
5. 程序自动将两种方法实现的相机内参、畸变系数以及每张图片的旋转向量、位移向量保存到上述的txt文件中
>**也可以将`cemeraBasicMain`中第9行`DEBUG`变量设为1，这是只用运行`cemeraBasicMain.py`，默认选择`.img/left`文件夹中的图片**
## 联系我
* 邮件：smzhgle@gmail.com



