# Camera Basic 单相机标定
## 功能说明
该程序通过相机拍摄的棋盘格图片进行相机标定，获得相机内参、畸变系数以及每张图片对应的旋转向量、位移向量。
## 代码文件夹结构
```
cameraBasic
│  calImpZhang.py    		#张友正标定的实现
│  cemeraBasicMain.py		#主程序，包括opencv标定
│  README.md
│  __init__.py
└─__pycache__
```
## 标定效果
### 选择文件夹
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/selectFloder.jpg)
### 找角点
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/chessBoardCorners.jpg)
### 去畸变
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/undistort.jpg)\
去畸变后的图片保存在`/reuslt/singleCal`
### 参数
参数见文件夹`/reuslt/singleCal/`