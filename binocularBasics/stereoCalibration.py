# 赵懿 2018/9/4
# 双摄像头标定
# 参考：https://blog.csdn.net/xuelabizp/article/details/50417914
# https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
import cameraBasic.cemeraBasicMain as cbm
import cv2 as cv
import numpy as np
import os
###----------------------自己实现的stereo标定------------------------###
# 对单个摄像机进行标定
# 输入：
# boradSize：棋盘格大小
# path；图片文件路径
# 输出
# cameraMatirx：相机内参
# disCoeffs,：畸变系数
# rvecs：旋转向量
# tvecs：位移向量
def singleCal(boardSize,path):
    filelist = cbm.getFilelist(path)
    imagePoints, objectCorners, imageSize = cbm.findPoints(filelist, boardSize)
    cameraMatirx, disCoeffs, rvecs, tvecs = cbm.cv_calibrate(imagePoints, objectCorners, imageSize)
    return cameraMatirx, disCoeffs, rvecs, tvecs
# 计算左侧相机到右侧相机的旋转和平移坐标
# 输入：
# rvls：旋转向量，左侧相机13
# rvrs：旋转向量，右侧相机13
# tvls：位移向量，左侧相机13
# tvrs：位移向量，右侧相机13
# 输出：
# Rs：左侧相机到右侧相机旋转矩阵13
# Ts：左侧相机到右侧相机位移矩阵13
def calcRt(rvls,tvls,rvrs,tvrs):
    Rs=[];Ts=[]
    for rvl, rvr in zip(rvls,rvrs):
        rmatl = cv.Rodrigues(rvl)[0]
        rmatr = cv.Rodrigues(rvr)[0]
        Rs.append(rmatr@rmatl.T)
    for tvl, R, tvr in zip(tvls, Rs, tvrs):
        Ts.append(tvr-R@tvl)
    #此处简单求了均值
    Rs=np.array(Rs).reshape((-1,3,3))
    Ts=np.array(Ts).reshape((-1,3))
    R=np.mean(Rs,0)
    T=np.mean(Ts,0)
    return R,T
# 计算基础矩阵
# 输入：
# Rs：左侧相机到右侧相机旋转矩阵13
# Ts：左侧相机到右侧相机位移矩阵13
# 输出
# Fs：基础矩阵13
def fundmentalMat(cml,cmr,R,t):
    cmlInv = np.linalg.inv(cml)
    cmrInvT = np.linalg.inv(cmr).T
    crosst=np.array([[0,-t[2],t[1]],[t[2],0,-t[0]],[-t[1],t[0],0]])
    F=cmrInvT@crosst@R@cmlInv
    F=F/F[2][2]
    return F
# 自己实现的stereo标定方法
def zhao_stereoCal(boardSize,pathl,pahtr):
    cml, dcl, rvls, tvls = singleCal(boardSize, pathl)
    cmr, dcr, rvrs, tvrs = singleCal(boardSize, pahtr)
    R, T = calcRt(rvls, tvls, rvrs, tvrs)
    F = fundmentalMat(cml,cmr,R,T)
    return R,T,F


###----------------------openCV的API进行stereo标定------------------------###
# 采用OpenCV的API进行立体视觉标定
def cv_stereoCal(boardSize,pathl,pathr):
    filelistl = cbm.getFilelist(pathl)
    filelistr = cbm.getFilelist(pathr)
    # 获得角点坐标
    imagePointsl, objectCornerls, imageSizel = cbm.findPoints(filelistl, boardSize)
    imagePointsr, objectCornerrs, imageSizer = cbm.findPoints(filelistr, boardSize)
    objectCorners=[]

    for i in range(len(filelistl)):
        objectCorners.append(objectCornerls)
        imagePointsl[i] = imagePointsl[i].reshape((-1,2))
        imagePointsr[i] = imagePointsr[i].reshape((-1, 2))
    # 获得camera matrix
    cml, dcl, rvls, tvls = cbm.cv_calibrate(imagePointsl, objectCornerls, imageSizel)
    cmr, dcr, rvrs, tvrs = cbm.cv_calibrate(imagePointsr, objectCornerrs, imageSizer)
    # 进行stereoCal,获得R,T,E,F

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F= cv.stereoCalibrate(objectCorners,
                           imagePointsl, imagePointsr,
                           cml, dcl, cmr, dcr,
                           imageSizel,
                           flags=cv.CALIB_FIX_INTRINSIC)
    #返回计算结果
    return cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F, imageSizel

def main(boardSize, pathl, pathr):
    cml, dcl, cmr, dcr, cvR, cvT, cvE, cvF, _ = cv_stereoCal(boardSize, pathl, pathr)
    if not os.path.exists('./result/'):
        os.mkdir('./result/')
    np.savetxt("./result/stereCal.txt",(cml, dcl, cmr, dcr, cvR, cvT, cvE, cvF),'%s',',','\n')

if __name__=="__main__":
    zhao_stereoCal((6,9),'../img/left','../img/right')
    main((6,9),'../img/left','../img/right')
