# Binocular Basic 双目相机视觉标定校正
## 功能说明
通过左右两相机拍摄图片进行两相机标定、立体视觉标定、立体校正
## 代码文件夹结构
```
binocularBasics
│  README.md
│  rectification.py         #立体校正，获得R1,R2,P1,P2,Q
│  stereoCalibration.py     #立体视觉标定，获得R,T,E,F
│  __init__.py
│
└─__pycache__
```
## 校正效果
![image](https://github.com/zhaone/ProjectStereo/blob/master/show/rectified.jpg)
参数见文件`/reuslt/stereoCal.txt`和`/reuslt/rectify.txt`
