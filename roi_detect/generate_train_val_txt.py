
import os
import random
import shutil
import cv2
from numpy.lib.type_check import imag
# if not os.path.exists("./data/train"):
#     os.makedirs("./data/train")
#     os.makedirs("./data/test")
#     os.makedirs("./data/annotations")
with open('anno_20211102.txt','r') as f:
    lines = f.readlines()

train_percent = 0.85
num = len(lines)
print("total images numbers:", num)  

list = range(num)
tr = int(num * train_percent)
train = random.sample(list, tr)
print("train size:", tr)

ftrain = open('./data/train.txt', 'w')
fval = open('./data/val.txt', 'w')

for i in list:
    name = lines[i]
    line = name.strip().split(',')
    # print(line)
    # break
    fn = line[0].split('/')[-1].replace("json","jpg")
    xywh = [int(x) for x in line[1].split(' ')]
    # x0,y0,w,h =  xywh[0]-20, xywh[1]-20,xywh[2]+40, xywh[3]+40
    # xywh = [20,20,xywh[2],xywh[3]]
    # # print(xywh)
    pts = [int(x) for x in line[2:]]

    # for j in range(len(pts)):
    #     if j%2==0:
    #         pts[j] = pts[j] -x0 +20 
    #     else:
    #         pts[j] = pts[j] -y0 +20
    
    # img = cv2.imread('data/coco/images_aug5/'+fn)
    # if x0-20<0 or y0-20<0 or y0+h+20>1599 or x0+w+20>1599:
    #     continue
    # roi = img[y0-20:y0+h+20,x0-20:x0+w+20]
    out = fn + " " + (',').join([str(a) for a in xywh]) +' '+(',').join([str(a) for a in pts]) +'\n'
    
    if i in train:
        # cv2.imwrite("data/coco_data/images/train/"+fn,img)
        shutil.copyfile('data/coco/img_aug5/'+fn,"data/coco_data/images/train/"+fn)
        ftrain.write(out)
    else:
        shutil.copyfile('data/coco/img_aug5/'+fn,"data/coco_data/images/val/"+fn)
        fval.write(out)

ftrain.close()
fval.close()
print("write finished!")
