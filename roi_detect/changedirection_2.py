'''
Descripttion: 
version: 1.0
Author: Ge Jun
Date: 2021-07-06 22:39:56
LastEditors: Ge Jun
LastEditTime: 2021-08-16 16:15:46
'''
import os
import cv2
import cv2
import numpy as np
import json
import math
from PIL import Image
from numpy.lib.function_base import angle
import base64
def decode_json(json_path):
    data = json.load(open(json_path, 'r', encoding='utf-8'))

    pts =[]
    pts2 =[]
    # img_w = data['imageWidth']
    # img_h = data['imageHeight']
    data["imagePath"]=""
    data["imageData"]= ""
    x, y, w, h = 0,0,0,0
    for s in data['shapes']:
        if len(s['points']) ==65:
            # for i in range(len(s['points'])):
            #     x = int(s['points'][i][0])
            #     y = int(s['points'][i][1])
            #     pts.append([y,x])
            #     pts2.append([x,y])
            for i in range(32):
                x = int(s['points'][i][0])
                y = int(s['points'][i][1])
                x_ = int(s['points'][64-i][0])
                y_ = int(s['points'][64-i][1])
                pts.append([y,x])
                pts.append([y_,x_])
                pts2.append([x,y])
                pts2.append([x_,y_])
            pts.append([int(s['points'][32][1]),int(s['points'][32][0])])
            pts2.append([int(s['points'][32][0]),int(s['points'][32][1])])
            if pts2:
                x, y, w, h = cv2.boundingRect(np.array(pts2))
    rotation = 0
    if pts:
        print(pts[0][0]-pts[-1][0],pts[-1][0] -pts[0][0],pts[0][1] - pts[-1][1])
        #上>下
        if pts[0][0]-pts[-1][0] > 300:
            rotation = -90
        #下>上
        if  pts[-1][0] -pts[0][0] > 300:
            rotation = 90
        #左大于右
        if   pts[0][1] - pts[-1][1] >300:
            rotation = -180
    return [y, x, y+h ,x+w],pts,data,rotation
            

#box为0~1的值，为[ymin, xmin, ymax, xmax]
#landmarks为0~1的值，为[y0,x0,y1,x1,y2,x2......yn,xn]
def change_direction(image, box, landmarks, angle):
    #为随机旋转的角度-90~90度
    theta = angle*(math.pi/180.0)
    
    #获取旋转的中心坐标
    #也即是图像的中心坐标
    image_height = image.shape[0]
    image_width = image.shape[1]
    scaler = np.stack([image_height, image_width], axis=0)
    center = np.reshape(0.5*scaler, [1, 2])
 
    #求旋转矩阵
    rotation = np.stack([np.cos(theta), np.sin(theta),-np.sin(theta), np.cos(theta)], axis=0)
    rotation_matrix = np.reshape(rotation, [2, 2])
 
    #旋转方框
    ymin, xmin, ymax, xmax = box
    h, w = ymax - ymin, xmax - xmin
    box = np.stack([ymin, xmin, ymin, xmax,ymax, xmax, ymax, xmin], axis=0)
    box = np.matmul(np.reshape(box, [4, 2]) - center, rotation_matrix) + center
    box = box
    y ,x  = box[:,0],box[:,1]
    ymin, ymax = np.min(y), np.max(y)
    xmin, xmax = np.min(x), np.max(x)
    box =np.stack([xmin, ymin, xmax, ymax], axis=0)
    
    #旋转坐标
    landmarks = np.matmul(landmarks - center, rotation_matrix) + center
    landmarks = landmarks[:,[1,0]]

    #旋转图像
    image = Image.fromarray(image)
    im_rotate = image.rotate(angle)
    im_rotate = np.array(im_rotate)
    return im_rotate, box, landmarks
 
if __name__ == "__main__":
    json_floder_path = '/home/think/文档/images/20210930/'

    json_names = os.listdir(json_floder_path)
    for json_name in json_names:
        if json_name.endswith('.json'):
            # json_name = "J21301521410-NG-20210523140620408-3.json"
            image = cv2.imread(json_floder_path+json_name.replace('.json','.jpg'))
            box, landmarks,data ,ang= decode_json(json_floder_path+json_name)
            if len(landmarks)==0:
                continue
            print(json_name)

            im_rotate, box, landmarks = change_direction(image, box, landmarks, ang)
            data['shapes'][0]['points'] = landmarks.tolist()

            data["imageData"]= string = base64.b64encode(cv2.imencode('.jpg', im_rotate)[1]).decode()

            with open('./data/coco/img_rotate5/'+json_name, 'w',encoding='utf-8') as f:
                json.dump(data, f)
            cv2.imwrite('./data/coco/img_rotate5/'+json_name.replace('.json','.jpg'), im_rotate)
        # cv2.imshow("image1",image )
        # cv2.imshow("image2",im_rotate)
        # cv2.waitKey(0)