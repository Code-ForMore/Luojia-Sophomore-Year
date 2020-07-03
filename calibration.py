import numpy as np
from cv2 import cv2
import glob
import yaml
import tkinter.filedialog

# 为什么有时会读取照片失败？OpenCV的imread只能读取英文路径下的文件，不能出现中文。
def calibrate():
    #棋盘角点数col*row
    col = 13
    row = 6

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((row * col, 3), np.float32)
    # 用于标定的棋盘每个方格边长为22mm
    objp[:, :2] = 22*np.mgrid[0:col, 0:row].T.reshape(-1, 2)

    objpoints = []  # 世界坐标系下的点坐标
    imgpoints = []  # 像素平面坐标系下的点坐标
    print("请选择标定用到的照片所在的文件夹", "\n")

    root = tkinter.Tk()
    root.withdraw()

    global path  # 用于标定的照片所在目录
    path = tkinter.filedialog.askdirectory(
        title="选择标定用到的照片所在的文件夹")  # 选择标定用到的照片所在的文件夹
    images = glob.glob(path+"/*.jpg")
    found = 0  # 记录用于标定的图像数目
    for k, fname in enumerate(images):
        img = cv2.imread(fname)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (col, row), None)
        # 角点检测

        if ret is True:
            print("读取", fname)
            objpoints.append(objp)

            
            # 角点检测精度会影响标定的精度
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)#亚像素角点位置
            # corners2=corners
            #_,corners2=cv2.find4QuadCornerSubpix(gray, corners, (11, 11))

            imgpoints.append(corners2)
            img = cv2.drawChessboardCorners(img, (col, row), corners2, ret)#标记角点
            found += 1
            if len(images) < 16:  # 图片过多时，不在UI中展示，避免弹窗过多
                cv2.namedWindow('press any key to continue', cv2.WINDOW_NORMAL)
                cv2.imshow('press any key to continue', img)
                cv2.waitKey(0)

            #image_name = path2 + "//corner"+str(found) + '.png'
            #cv2.imwrite(image_name, img)
            #存储已标出角点的照片
            
    global path2  # 存放结果的目录（含记录相机参数的文件，和畸变矫正后的照片，3-D box照片）
    path2 = tkinter.filedialog.askdirectory(
        title="选择结果存放的文件夹(应与用于标定的照片所在的文件夹不同)")  # 选择结果存放的文件夹

    print("Number of images used for calibration: ", found)

    # 相机标定
    ret2, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                        gray.shape[::-1], None, None)

    print("reprojection error:", ret2)
    print("内参矩阵:", mtx)
    print("畸变系数：", dist)
    print("旋转向量：", rvecs)
    print("平移向量：", tvecs)

    images = glob.glob(path+"//*.jpg")
    for i, fname in enumerate(images):
        img = cv2.imread(fname)
        if img is None:
            continue
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1,
                                                            (w, h))
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)  # 矫正畸变

        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]#裁剪
        outpath = path2+"//tianyi_gao_undistorted" + str(i + 1) + ".jpg"
        cv2.imwrite(outpath, dst)
    print("新内参矩阵：", newcameramtx)
    
    data = {
        'camera_matrix': np.asarray(mtx).tolist(),
        'dist_coeff': np.asarray(dist).tolist(),
        'new_camera_matrix': np.asarray(newcameramtx).tolist(),
        'rvecs': np.asarray(rvecs).tolist(),
        'tvecs': np.asarray(tvecs).tolist(),
        'reprojection_error': np.asarray(ret2).tolist()
    }
    # 存储相机参数(yaml)
    with open(path2+"//calibration_parameters.yaml", "w") as f:
        yaml.dump(data, f)
    # 存储相机参数(txt)
    with open(path2+"//tianyi_gao_cam.txt", "w") as f2:
        name = list(data.keys())
        value = list(data.values())
        for i in range(len(name)):
            f2.write(name[i] + ":" + "\n" + str(value[i]) + "\n")

    print('Calibrate Done')
    cv2.destroyAllWindows()
    return mtx, dist, rvecs, tvecs, ret2, path2
    # done

#在图片中画出3-D坐标轴
def drawAxis(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 3)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 3)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 3)
    return img

#在图片中画出3-D Box
def drawBox(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    #img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 255), -3)
    for i in range(4):
        j = (i+1) % 4
        img = cv2.line(img, tuple(imgpts[i]), tuple(
            imgpts[j]), (255, 255, 0), 2)

    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(
            imgpts[j]), (255, 255, 0), 2)

    for i in range(4, 8):
        j = (i+1) % 4+4
        img = cv2.line(img, tuple(imgpts[i]), tuple(
            imgpts[j]), (255, 255, 0), 2)
    #img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 255, 255), 3)
    return img



def AxisAndBox():
    # 读取相机参数
    with open(path2+'//calibration_parameters.yaml') as file:
        documents = yaml.full_load(file)
    data = list(documents.values())
    mtx = np.asarray(data[2])
    #dist = np.asarray(data[1])

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((13 * 6, 3), np.float32)
    objp[:, :2] = np.mgrid[0:13, 0:6].T.reshape(-1, 2)
    axis = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                        [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])
    axis2 = np.float32([[4, 0, 0], [0, 4, 0], [0, 0, -4]]).reshape(-1, 3)
    
    num = 0  # 计数器
    images2 = glob.glob(path2+'//tianyi_gao_undistorted*.jpg')
    for fname in images2:
        num = num+1
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (13, 6), None)
        if ret is True:
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)

            # 计算外参,估计相机位姿
            _, rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, None)
            
            # 将3-D点投影到像平面
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, None)
            imgpts2, jac2 = cv2.projectPoints(axis2, rvecs, tvecs, mtx, None)
            img = drawBox(img, corners2, imgpts)
            img = drawAxis(img, corners2, imgpts2)
            cv2.imwrite(path2+"//tianyi_gao_"+str(num)+".jpg", img)
            if len(images2) < 16:  # 图片过多时，不在UI中展示
                cv2.namedWindow('press any key to continue', cv2.WINDOW_NORMAL)
                cv2.imshow('press any key to continue', img)
                cv2.waitKey(0)
    print('Draw Done')
    cv2.destroyAllWindows()
    return num, path2#返回处理图片数和结果存储路径
