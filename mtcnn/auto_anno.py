'''
Created on May 20, 2018

@author: pinnacle
'''
from PIL import ImageDraw
import anno_parse as ap
import mtcnn.detector as det
import os
import sys
import time
import numpy as np
import image_process as ip
import matplotlib.pylab as plt

def detect_test(path):
    for f in os.listdir(path):
        p=os.path.join(path,f)
        image = ip.image_to_3channels(p,True)
        if image is None:
            continue
        start=time.clock()
        bounding_boxes, landmarks = det.detect_faces(image)
        end=time.clock()
        print "take %sms"%(1000*end-1000*start),"num faces:",len(bounding_boxes)
        if len(bounding_boxes)>0:
            draw=ImageDraw.Draw(image)
            
            for bbox in bounding_boxes:
                bbox=(bbox[0],bbox[1],bbox[2],bbox[3])
                draw.rectangle(bbox,outline="red")
            
            plt.imshow(image)
            plt.show()

def auto_anno(dir_path):
    for f in os.listdir(dir_path):
        p=os.path.join(dir_path,f)
        print p
        if ".xml" in p:
            continue
        image = ip.image_to_3channels(p,True)
        if image is None:
            continue
        start=time.clock()
        bounding_boxes, landmarks = det.detect_faces(image)
        end=time.clock()
        print "take %sms"%(1000*end-1000*start),"num faces:",len(bounding_boxes)
        if len(bounding_boxes)>0:
            bounding_boxes=[[bbox[0],bbox[1],bbox[2],bbox[3]] for bbox in bounding_boxes]
            bounding_boxes=np.round(bounding_boxes)
            bounding_boxes=np.asarray(bounding_boxes,np.int)

            ap.save_anno_to_xml(p,image.size[0],image.size[1],3,annos=bounding_boxes)
            
        
if __name__=="__main__":
    if len(sys.argv)==3:
        if sys.argv[1]=="test":
            detect_test(sys.argv[2])
        elif sys.argv[1]=="anno":
            auto_anno(sys.argv[2])
    else:
        print 'Usage: python auto_anno.py test image_dir_path'
        print 'Usage: python auto_anno.py anno image_dir_path'
    
    
    
    