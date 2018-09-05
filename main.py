#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
2018/9/5 赵懿
项目主程序（未完成，不包含第三部分）
'''
import sys
import getopt
import os
import re
import tkinter.filedialog
import binocularBasics.stereoCalibration as bstc
import binocularBasics.rectification as bref
import cameraBasic.cemeraBasicMain as ccbm
import cameraBasic.calImpZhang as czhang
'''
功能：
-c 对单个相机进行标定
-u 对图片进行去畸变操作
-s 对两个相机记性立体标定
-r 对两个相机进行立体纠正
-b 设置棋盘格大小
-z 比较自己实现的张氏标定和openCV对单个相机标定的结果
-h 帮助
'''
# 主程序，选择相应功能
def main(argv):
    boardSize=[6,9]
    try:
        opts, args = getopt.getopt(argv, "hcusrzb:")
    except:
        help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit(0)
        elif opt in ("-b"):
            figures=re.findall(r"\d+",arg)
            if(len(figures)!=2):
                print("boardSize设置错误，应为 'row*col'")
                sys.exit(-2)
            boardSize[0]=int(figures[0])
            boardSize[1]=int(figures[1])
        elif opt in ("-c"):
            singleCal(tuple(boardSize))
        elif opt in ("-u"):
            undistort(tuple(boardSize))
        elif opt in ("-s"):
            stereoCalibrate(tuple(boardSize))
        elif opt in ("-r"):
            rectificate(tuple(boardSize))
        elif opt in ("-z"):
            campare(tuple(boardSize))
        else:
            sys.exit(0)

# 对单个相机进行标定
def singleCal(boardSize):
    if DEBUG==1:
        filelist = ccbm.getFilelist('./img/left')
    else:
        dirname = tkinter.filedialog.askdirectory(initialdir='./', title="请选择图片文件夹")
        filelist = ccbm.getFilelist(dirname)
        if (len(filelist) < 3):
            print("提供的图片数目过少，请至少保证有3张图片！")
            os._exit(-1)
    ccbm.main(boardSize,filelist)
# 比较自己实现的张氏标定和openCV对单个相机标定的结果
def campare(boardSize):
    if DEBUG==1:
        filelist = ccbm.getFilelist('./img/left')
    else:
        dirname = tkinter.filedialog.askdirectory(initialdir='./', title="请选择图片文件夹")
        filelist = getFilelist(dirname)
        if (len(filelist) < 3):
            print("提供的图片数目过少，请至少保证有3张图片！")
            os._exit(-1)
    czhang.main(boardSize,filelist)
# 对图片进行去畸变操作
def undistort(boardSize):
    if DEBUG==1:
        filelist = ccbm.getFilelist('./img/left')
    else:
        dirname = tkinter.filedialog.askdirectory(initialdir='./', title="请选择图片文件夹")
        filelist = getFilelist(dirname)
        if (len(filelist) < 3):
            print("提供的图片数目过少，请至少保证有3张图片！")
            os._exit(-1)
    ccbm.undistort(boardSize,filelist)
# 对两个相机记性立体标定
def stereoCalibrate(boardSize):
    if DEBUG == 1:
        pathl = './img/left'
        pathr = './img/right'
    else:
        pathl = tkinter.filedialog.askdirectory(initialdir='./', title="请选择第一个文件夹")
        pathr = tkinter.filedialog.askdirectory(initialdir='./', title="请选择第二个文件夹")
    bstc.main(boardSize,pathl,pathr)
# 对两个相机进行立体纠正
def rectificate(boardSize):
    if DEBUG == 1:
        pathl = './img/left'
        pathr = './img/right'
    else:
        pathl = tkinter.filedialog.askdirectory(initialdir='./', title="请选择第一个文件夹")
        pathr = tkinter.filedialog.askdirectory(initialdir='./', title="请选择第二个文件夹")
    bref.main(boardSize,pathl,pathr)
# 帮助
def help():
    print("-h 帮助：（以下不设置棋盘格大小，则默认为'6 9',除-b外，其他命令不需要加参数）\n")
    print('-b 设置棋盘格大小\n'
          "格式：-b 'row col'，即单引号 行数 列数 单引号，row和col为棋盘格角点行数和列数\n"
          '写参数时需要先写-b ，即先设置boardSize，再加其他参数')
    print('-c 对单个相机进行标定\n'
          '（需要设置-b 棋盘格大小）\n'
          '结果保存在 result/singleCal/ 文件夹下\n'
          'result/singleCal/cameraMatrix.txt 相机内矩阵\n'
          'result/singleCal/disCoeffs.txt 相机畸变参数(k1,k2,k3,p1,p2)\n'
          'result/singleCal/revecs.txt 每张图片的旋转矩阵，每行对应文件夹中对应顺序图片\n'
          'result/singleCal/tevecs.txt 每张图片的位移矩阵，每行对应文件夹中对应顺序图片\n')
    print('-u 对文件夹中图片进行去畸变操作\n'
          '（需要设置-b 棋盘格大小）\n'
          '结果保存在 result/undisort/ 文件夹下\n')
    print('-s 对两个相机进行立体视觉标定\n'
          '（需要设置-b 棋盘格大小）\n'
          '结果保存在 result/stereCal.txt 文件中\n'
          '从上到下依次是左相机内矩阵, 左相机畸变参数, 左相机内矩阵, 左相机畸变参数, 旋转矩阵, 位移矩阵, 本质矩阵, 基础矩阵\n')
    print('-r 对两个相机进行立体纠正\n'
          '（需要设置-b 棋盘格大小）\n'
          '结果保存在 result/rectify.txt 文件中\n'
          '从上到依次是左相机旋转矩阵, 右相机旋转矩阵, 左相机新的投影矩阵, 右相机新的投影矩阵, disparity-to-depth mapping matrix\n')
    print('-z 比较自己实现的张氏标定和openCV对单个相机标定的结果\n'
          '结果保存在result/compare/ 文件夹下\n'
          'openCV文件夹保存openCV API的结果，zhang文件夹保存自己实现的张氏标定的结果\n')

if __name__=='__main__':
    DEBUG=1
    main(sys.argv[1:])
