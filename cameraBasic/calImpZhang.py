# 赵懿 2018/8/30
# 张氏标定方法实现

# BUG：畸变系数计算得不太准确^_^|||
import cv2 as cv
import numpy as np
import math
# 计算单应矩阵
# 输入：
# imagePoints：13*(54*2)的array，所有图片的角点坐标
# objectCorners：13*(54*3) 世界坐标系中角点坐标
# 输出：
# H：13个h，hi是第i符图片的单应矩阵(3*3)
def homographys(imagePoints, objectCorners):
    H = []
    for imagePoint in imagePoints:
        imagePoint=np.array(imagePoint,np.float32)
        h, _ = cv.findHomography(objectCorners[:, :2], imagePoint)
        H.append(h)
    return H
# 计算Vb的V矩阵
# 输入：
# H:homographys的输出，所有单应矩阵
# 输出：
# V：paper中计算camera的矩阵V
def getV(H):
    V=[]
    for h in H:
        v=np.zeros((4,6))
        for i in range(2):
            for j in range(2):
                v[2*i+j]=np.array([h[0][i] * h[0][j], h[0][i] * h[1][j] + h[1][i] * h[0][j],
                     h[1][i] * h[1][j], h[2][i] * h[0][j] + h[0][i] * h[2][j],
                     h[2][i] * h[1][j] + h[1][i] * h[2][j], h[2][i] * h[2][j]])
        V.append(v[1])
        V.append(v[0]-v[3])
    V=np.array(V)
    return V
# 计算获得相机矩阵CameraMatrix
# 输入：
# V：getV函数输出，paper中计算camera的矩阵V
# 输出：
# CameraMatrix：相机内参矩阵
def getCameraMatrix(V):
    _, B = np.linalg.eig(V.T @ V)
    B = B[:, -1]
    v0 = (B[1]*B[3]-B[0]*B[4])/(B[0]*B[2]-B[1]*B[1])
    lamda = B[5]-(B[3]*B[3]+v0*(B[1]*B[3]-B[0]*B[4]))/B[0]
    alpha = math.sqrt(lamda/B[0])
    beta = math.sqrt(lamda*B[0]/(B[0]*B[2]-B[1]*B[1]))
    gama = -B[1]*alpha*alpha*beta/lamda
    u0 = gama*v0/alpha-B[3]*alpha*alpha/lamda
    CameraMatrix = np.array([alpha,gama,u0,0,beta,v0,0,0,1]).reshape(3, 3)
    return CameraMatrix
# 获得旋转向量和位移向量
# 输入：
# H:homographys的输出，所有单应矩阵
# CameraMatrix：相机内参矩阵
# 输出：
# Rtvecs：paper中的[r1,r2,t]，不包含r3,用于计算畸变
# rmat：旋转矩阵，3*3（后面会化成旋转向量）
# tvecs：位移向量，3*1
def getRtvecs(H,CameraMatrix):
    Rtvecs=[]
    rmat=[]
    tvecs=[]
    inv=np.linalg.inv(CameraMatrix)
    for h in H:
        # 单位化（归一化）
        orivec=inv@h[:,0]
        lamda=1/math.sqrt(orivec.T@orivec)
        tmp=inv@h
        Rt=lamda*inv@h
        t=Rt[:,2].copy()
        Rt[:,2]=Rt[:,0]*Rt[:,1]
        #奇异值分解
        U, sigma, VT = np.linalg.svd(Rt)
        Rt=U@VT
        rmat.append(Rt)
        tvecs.append(t)
        Rtvecs.append(np.hstack((Rt[:,:2],t.reshape((3,1)))))
    return Rtvecs,rmat,tvecs
# 获得计算畸变系数
# 输入：
# CameraMatrix：相机内参矩阵
# imagePoints：13*(54*2)的array，所有图片的角点坐标
# objectCorners：13*(54*3) 世界坐标系中角点坐标
# Rtvecs：paper中的[r1,r2,t]，不包含r3,用于计算畸变
# 输出：
# disCoeffs：畸变系数 [k1,k2,0,0,0]
def getDisCoeffs(CameraMatrix,imagePoints,objectCorners,Rtvecs):
    #计算无畸变的(x,y)
    xys=[]
    for rtvec in Rtvecs:
        mat=np.array(objectCorners).reshape((-1,3))
        mat[:,2]=1
        xy=rtvec@mat.T
        xys.append(xy)
    xys=tuple(xys)
    xys=np.hstack(xys)
    # 计算无畸变的(u,v)
    idealUV=CameraMatrix@xys
    idealUV=idealUV/idealUV[2]
    idealUV=idealUV[:2].T
    # 计算d=(真实u-理想u,真实v-理想v)
    imagePointsMat=[]
    for imagePoint in imagePoints:
        imagePoint = imagePoint.reshape((54, 2))
        imagePointsMat.append(imagePoint)
    imagePointsMat=tuple(imagePointsMat)
    imagePointsMat=np.vstack(imagePointsMat)

    d=imagePointsMat-idealUV#(真u,v-理想u,v),(702,2)
    d=np.hstack((d[:,0],d[:,1])).reshape((-1,1))
    #计算D
    tmp=xys[:2,:]*xys[:2,:]
    power1=tmp[0,:]+tmp[1,:]#x2+y2
    power2=power1*power1#(x2+y2)2
    power1=power1.reshape((-1, 1))
    power2=power2.reshape((-1, 1))
    idealUV[:,0] = idealUV[:,0] - CameraMatrix[0, 2]#u-u0
    idealUV[:,1] = idealUV[:,1] - CameraMatrix[1, 2]#v-v0
    idealUV=idealUV.reshape((idealUV.shape[0],idealUV.shape[1],1))
    idealUVcopy=idealUV.copy()
    idealUV[:,0]=idealUV[:,0]* power1#(u-u0)*(x2+y2)
    idealUV[:,1] = idealUV[:,1] * power1#(v-v0)*(x2+y2)
    idealUVcopy[:,0] = idealUVcopy[:,0] * power2#(u-u0)*(x2+y2)2
    idealUVcopy[:,1] = idealUVcopy[:,1] * power2#(v-v0)*(x2+y2)2
    D1 = np.vstack((idealUV[:,0],idealUV[:,1]))
    D2 = np.vstack((idealUVcopy[:,0],idealUVcopy[:,1]))
    D=np.hstack((D1,D2))
    #解方程Dk=d
    k=np.linalg.inv(D.T@D)@D.T@d

    disCoeffs=np.array([k[0][0],k[1][0],0,0,0]).reshape((1,5))
    return disCoeffs
# 旋转矩阵转旋转向量，此处调用了opencv的API
# 输入：
# rmat：旋转矩阵
# 输出：
# revecs：旋转向量
def ramt2rvecs(rmat):
    revecs=[]
    for mat in rmat:
        revec=np.zeros((3,1))
        cv.Rodrigues(mat,revec)
        revecs.append(revec)
    return revecs
# 标定总流程
# 输入：
# imagePoints：13*(54*2)的array，所有图片的角点坐标
# objectCorners：13*(54*3) 世界坐标系中角点坐标
# 输出：
# cameraMatirx：相机内参
# disCoeffs,：畸变系数
# rvecs：旋转向量
# tvecs：位移向量
def zhangCalibrateCamera(imagePoints,objectCorners):
    # 计算单应矩阵
    H=homographys(imagePoints, objectCorners)
    # 计算V矩阵
    V=getV(H)
    # 计算相机内参
    cameraMatirx = getCameraMatrix(V)
    # 计算旋转、位移向量
    RTvecs, rmat, tvecs = getRtvecs(H,cameraMatirx)
    # 计算旋转、位移向量
    disCoeffs = getDisCoeffs(cameraMatirx,imagePoints, objectCorners, RTvecs)
    # 将位移矩阵转化为向量
    rvecs=ramt2rvecs(rmat)
    return cameraMatirx, disCoeffs, rvecs, tvecs



