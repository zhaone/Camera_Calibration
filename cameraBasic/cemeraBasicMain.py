# 赵懿 2018/8/29
# camera Basic主程序
import os
import cv2 as cv
import numpy as np
import tkinter.filedialog
import cameraBasic.calImpZhang as zhang

DEBUG=1
# 获得图片目录名
# 输入：
# path：图片文件夹
# 输出：
# filelist：图片文件路径名
def getFilelist(path):
    filelist=[]
    files=os.listdir(path)
    for file in files:
        filelist.append(os.path.join(path,file))
    return filelist
# 找到角点每幅图角点坐标，以及初始化角点的世界坐标系坐标
# 输入：
# filelist：图片文件路径名
# boardSize：一个tuple(棋盘格行数，棋盘格列数)
# 输出：
# imagePoints：所有图像的角点位置list[array(boardSize)]
# objectCorners：世界角点坐标array(boardSize)
def findPoints(filelist,boardSize):
    # 首先计算所有图像的角点位置
    imagePoints=[]
    imageSize=(0,0)
    for file in filelist:
        image = cv.imread(file)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        imageSize=image.shape
        _ , imageCorners=cv.findChessboardCorners(image,boardSize)
        imageCorners=cv.cornerSubPix(image, imageCorners, (5, 5), (-1, -1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imagePoints.append(imageCorners)
    # 初始化世界角点坐标
    objectCorner =[]
    for j in range(boardSize[1]):
        for i in range(boardSize[0]):
            objectCorner.append([i+1,j+1,0])
    objectCorners=np.array(objectCorner, np.float32)
    return imagePoints,objectCorners,imageSize
# 相机标定
# 输入：
# imagePoints：所有图像的角点位置list[array(boardSize)]
# objectCorners：世界角点坐标array(boardSize)
# imageSize：图片大小
# 输出：
# cameraMatirx：相机内参
# disCoeffs：畸变系数
# rvecs：旋转矩阵
# tvecs：位移向量
def cv_calibrate(imagePoints,objectCorners,imageSize):
    objectPoints=[]
    for i in range(len(imagePoints)):
        objectPoints.append(objectCorners)
    _,cameraMatirx, disCoeffs, rvecs, tvecs=cv.calibrateCamera(objectPoints,imagePoints,imageSize,None,None)
    return cameraMatirx, disCoeffs, rvecs, tvecs
# 去畸变
# 输入：
# filelist：需要去畸变的图像文件目录名
# cameraMatirx：相机内参
# disCoeffs：畸变系数
def undistort(filelist,cameraMatirx,disCoeffs):
    for file in filelist:
        image=cv.imread(file)
        cv.imshow("去畸变前",image)
        undisImage=cv.undistort(image,cameraMatirx,disCoeffs)
        cv.imshow("去畸变后", undisImage)
        cv.waitKey(-1)
# 保存标定参数
# 输入：
# path：保存路径
# method：是opencv还是自己实现的张的方法
# cameraMatirx, mdisCoeffs, rvecs, tvecs：四个标定参数
def save(path, method, cameraMatirx, disCoeffs, rvecs, tvecs):
    dirname=os.path.join(path, method)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    np.savetxt(os.path.join(dirname, "cameraMatirx.txt"), cameraMatirx)
    np.savetxt(os.path.join(dirname, "disCoeffs.txt"), disCoeffs)
    np.savetxt(os.path.join(dirname, "rvecs.txt"), rvecs)
    np.savetxt(os.path.join(dirname, "tvecs.txt"), tvecs)

if __name__=='__main__':
    if DEBUG==0:
        #首先获得数据
        dirname=tkinter.filedialog.askdirectory(initialdir='./',title="请选择图片文件夹")
        filelist=getFilelist(dirname)
        if (len(filelist)<3):
            print("提供的图片数目过少，请至少保证有3张图片！")
            os._exit(-1)
        row=input("棋盘格行数：")
        col=input("棋盘格列数：")
        #设置boardSize
        boardSize = (int(row), int(col))
    else:
        boardSize = (6,9)
        filelist = getFilelist('./img/left')

    imagePoints, objectCorners, imageSize=findPoints(filelist, boardSize)
    cameraMatirx, disCoeffs, rvecs, tvecs=cv_calibrate(imagePoints,objectCorners,imageSize)
    zcameraMatirx, zdisCoeffs, zrvecs, ztvecs = zhang.zhangCalibrateCamera(imagePoints, objectCorners)

    save('./compare', 'opencv', cameraMatirx, disCoeffs, rvecs, tvecs)
    save('./compare', 'zhang', zcameraMatirx, zdisCoeffs, zrvecs, ztvecs)

    undistort(filelist,cameraMatirx,disCoeffs)