# 赵懿 2018/8/29
# camera Basic主程序
import os
import cv2 as cv
import numpy as np

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
        found , imageCorners=cv.findChessboardCorners(image,boardSize)
        imageCorners=cv.cornerSubPix(image, imageCorners, (11, 11), (-1, -1), (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        DEBUG=0
        if DEBUG==1:
            cv.drawChessboardCorners(image, boardSize, imageCorners, found)
            cv.imshow("chessboard corners",image)
            cv.waitKey(-1)
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
def undistort(boardSize,filelist):
    imagePoints, objectCorners, imageSize = findPoints(filelist, boardSize)
    cameraMatirx, disCoeffs, rvecs, tvecs = cv_calibrate(imagePoints, objectCorners, imageSize)
    save('./result/singleCal', cameraMatirx, disCoeffs, rvecs, tvecs)
    for file in filelist:
        image=cv.imread(file)
        cv.imshow("before undistort",image)
        undisImage=cv.undistort(image,cameraMatirx,disCoeffs)
        cv.imshow("after undistort", undisImage)
        if not os.path.exists('./result/undisort'):
            os.makedirs('./result/undisort')
        cv.imwrite(os.path.join('./result/undisort',os.path.basename(file)) , undisImage)
        cv.waitKey(-1)
# 保存标定参数
# 输入：
# path：保存路径
# method：是opencv还是自己实现的张的方法
# cameraMatirx, mdisCoeffs, rvecs, tvecs：四个标定参数
def save(dirname, cameraMatirx, disCoeffs, rvecs, tvecs):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    np.savetxt(os.path.join(dirname, "cameraMatirx.txt"), cameraMatirx)
    np.savetxt(os.path.join(dirname, "disCoeffs.txt"), disCoeffs)
    np.savetxt(os.path.join(dirname, "rvecs.txt"), rvecs)
    np.savetxt(os.path.join(dirname, "tvecs.txt"), tvecs)

def main(boardSize,filelist):
    imagePoints, objectCorners, imageSize = findPoints(filelist, boardSize)
    cameraMatirx, disCoeffs, rvecs, tvecs = cv_calibrate(imagePoints, objectCorners, imageSize)
    save('./result/singleCal', cameraMatirx, disCoeffs, rvecs, tvecs)

if __name__=='__main__':
    filelist = getFilelist('../img/left')
    main((6,9),filelist)