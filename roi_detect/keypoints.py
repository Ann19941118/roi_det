
from datetime import date
import json
import os
import cv2
import numpy as np

txt_name = './anno_20211102.txt'
txt_file = open(txt_name, 'w',encoding='utf-8')         
 
def decode_json(json_floder_path,json_name):

    json_path = os.path.join(json_floder_path, json_name)
    with open(json_path, 'r') as f:
        data = json.load(f)
    # img_w = data['imageWidth']
    # img_h = data['imageHeight']
    for s in data['shapes']:
        if len(s['points']) ==65:
            # print(len(s['points']))
            # print(json_name)
            pts =[]
            pts2 = []
            for i in range(len(s['points'])):
                x = int(s['points'][i][0])
                y = int(s['points'][i][1])
                pts.append(x)
                pts.append(y)
                pts2.append([x,y])

            if pts:
                x, y, w, h = cv2.boundingRect(np.array(pts2))
                if pts2[0][0]-pts2[-1][0] > 300:
                    pts2.reverse()
                    pts = [pts2[i][j] for i in range(len(pts2)) for j in range(2)]
            txt_file.write(json_path +"," +str(x-30)+" "+str(y-30)+" "+str(w+60)+" "+str(h+60)+",")
            txt_file.write(",".join([str(a) for a in pts]))
            txt_file.write('\n')
 
    
if __name__ == "__main__":
    
    json_floder = '/home/think/文档/roi_det/data/coco/img_aug5'
    # json_floders = ['/home/think/文档/yolov5/data/coco/img_aug','/home/think/文档/yolov5/data/coco/img_aug2','/home/think/文档/yolov5/data/coco/img_aug3']
    # json_floders = ['/home/think/文档/yolov5/data/coco/img_aug']
    # for floder in json_floder:
            
    json_names = os.listdir(json_floder)
    for json_name in json_names:
        if json_name.endswith('.json'):
            decode_json(json_floder,json_name)
    txt_file.close()