# 赵懿 2018/9/5
# 立体纠校正
# 参考：https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html
import cv2 as cv
import numpy as np
import binocularBasics.stereoCalibration as stc
import cameraBasic.cemeraBasicMain as ccb
import os
'''
获得校正之后的两个相机的map
输入：
boardSize：棋盘格大小
leftPath：左侧相机照片文件夹
rightPath：右侧相机照片文件夹
输出：
leftMaps：左侧相机的map
rightMaps：右侧相机的map
'''
def getMaps(boardSize,leftPath,rightPath):
    #获得内矩阵、畸变参数以及R, T, E, F
    cml, dcl, cmr, dcr, R, T, E, F, imageSize = \
        stc.cv_stereoCal(boardSize, leftPath, rightPath)
    Rl, Rr, Pl, Pr, Q, validPixROI1, validPixROI2 = \
        cv.stereoRectify(cml, dcl, cmr, dcr, imageSize, R, T, 0, (0, 0))
    leftMaps = cv.initUndistortRectifyMap(
        cml, dcl, Rl, Pl, (imageSize[1], imageSize[0]), cv.CV_16SC2)
    rightMaps = cv.initUndistortRectifyMap(
        cmr, dcr, Rr, Pr, (imageSize[1], imageSize[0]), cv.CV_16SC2)
    return leftMaps,rightMaps, Rl, Rr, Pl, Pr, Q
'''
检测校正效果
输入：
boardSize：棋盘格大小
leftMaps：左侧相机的map
rightMaps：右侧相机的map
leftImagePath：左侧相机照片路径
rightImagePath：右侧相机照片路径
'''
def check(boardSize,leftMaps,rightMaps,leftImagePath,rightImagePath):
    imagel = cv.imread(leftImagePath)
    imager = cv.imread(rightImagePath)
    imageSize = imagel.shape
    imagelrmap = cv.remap(imagel, leftMaps[0], leftMaps[1], cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    imagerrmap = cv.remap(imager, rightMaps[0], rightMaps[1], cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    imageShowl = cv.resize(imagelrmap, (imageSize[1], imageSize[0]), 0, 0, cv.INTER_AREA)
    imageShowr = cv.resize(imagerrmap, (imageSize[1], imageSize[0]), 0, 0, cv.INTER_AREA)
    imageShow = np.hstack((imageShowl, imageShowr))
    for i in range(0, imageShow.shape[0], 16):
        cv.line(imageShow, (0, i), (imageShow.shape[1], i), (0, 0, 255), 1, 8)
    cv.imshow('rectified', imageShow)
    cv.waitKey(-1)

def main(boardSize,pathl,pathr):
    leftMaps, rightMaps, Rl, Rr, Pl, Pr, Q = getMaps(boardSize, pathl, pathr)
    filelist1 = ccb.getFilelist(pathl)
    filelist2 = ccb.getFilelist(pathr)
    file1 = filelist1[int(len(filelist1) / 2)]
    file2 = filelist2[int(len(filelist2) / 2)]
    check(boardSize, leftMaps, rightMaps, file1, file2)
    if not os.path.exists('./result/'):
        os.mkdir('./result/')
    np.savetxt("./result/rectify.txt",(Rl, Rr, Pl, Pr, Q),'%s',',','\n')

if __name__=="__main__":
    main((6,9),'./img/left','./img/right')