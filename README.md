# ProjectStereo 
## 功能说明
该程序
* cameraBasic：通过单相机拍摄的棋盘格图片进行相机标定，获得相机内参、畸变系数以及每张图片对应的旋转向量、位移向量。
* binocularBasics：通过左右两相机拍摄图片进行两相机标定、立体视觉标定、立体校正
* 深度估计（待补充）
## 代码文件夹结构
```
ProjectStereo 
├─.idea
├─binocularBasics   #两相机标定、立体视觉标定、立体校正
│  └─__pycache__
├─cameraBasic       #单相机标定，获得相机内参、畸变系数、旋转向量、位移向量
│  └─__pycache__
├─img               #图片文件夹
│  ├─left           #左侧相机拍摄图片
│  └─right          #右侧相机拍摄图片
├─report            #report的tex
│  └─figures
├─result            #程序结果文件夹，结果都保存在这个文件夹
│  ├─compare        #自己实现的张氏标定和openCV的比较
│  │  ├─opencv
│  │  └─zhang
│  ├─singleCal      #单相机标定
│  ├─undisort       #去畸变后的图片
│  ├─rectify.txt    #立体校正后得到的参数
│  └─stereCal.txt   #立体视觉标定后得到的参数
└─show              
```
## 程序使用方法
>**运行方式：python main.py -bhcusrz（参数）**\
>**程序默认设置DEBUG为1，不用设置boardSize，即默认设置boradSize是(6,9)，单相机标定采用img/left中的图片，两台相机采用img/left和img/right中的图片**\
>**main.py中DEBUG设置为0，则可以设置boradSize，选择图片文件夹**\
>**有图片弹出时按任意键可以继续**
##参数：-bhcusrz
1. -h 帮助\
`python main.py -h`\
输出参数帮助
2. -b 设置棋盘格大小\
`python main.py -b 'row col'`\
格式：-b 'row col'，即单引号 行数 列数 单引号，row和col为棋盘格角点行数和列数\
写参数时需要先写-b ，即先设置boardSize，再加其他参数
3. -c 对单个相机进行标定\
`python main.py -c`（需要设置-b 棋盘格大小）\
结果保存在 `result/singleCal/` 文件夹下：\
`result/singleCal/cameraMatrix.txt` 相机内矩阵\
`result/singleCal/disCoeffs.txt` 相机畸变参数(k1,k2,k3,p1,p2)\
`result/singleCal/revecs.txt` 每张图片的旋转矩阵，每行对应文件夹中对应顺序图片\
`result/singleCal/tevecs.txt` 每张图片的位移矩阵，每行对应文件夹中对应顺序图片\
4. -u 对文件夹中图片进行去畸变操作\
`python main.py -u`（需要设置-b 棋盘格大小）\
结果保存在 result/undisort/ 文件夹下
5. -s 对两个相机进行立体标定\
`python main.py -s`（需要设置-b 棋盘格大小）\
结果保存在 result/stereCal.txt 文件中\
从上到下依次是左相机内矩阵, 左相机畸变参数, 左相机内矩阵, 左相机畸变参数, 旋转矩阵, 位移矩阵, 本质矩阵, 基础矩阵
6. -r 对两个相机进行立体纠正\
`python main.py -r`（需要设置-b 棋盘格大小）\
从上到依次是左相机旋转矩阵, 右相机旋转矩阵, 左相机新的投影矩阵, 右相机新的投影矩阵, disparity-to-depth mapping matrix
结果保存在 result/rectify.txt 文件中\
7. z 比较自己实现的张氏标定和openCV对单个相机标定的结果\
`python main.py -z`（需要设置-b 棋盘格大小）\
结果保存在result/compare/ 文件夹下\
openCV文件夹保存openCV API的结果，zhang文件夹保存自己实现的张氏标定的结果

## 联系我
* 邮件：yizhaome@gmail.com