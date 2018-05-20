'''
Created on May 20, 2018

@author: pinnacle
'''
import anno_parse as ap
import mtcnn.detector as det
import os
import time
import numpy as np
import image_process as ip

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
            
def to_wider_face_anno(dir_path):
    for f in os.listdir(dir_path):
        p=os.path.join(dir_path,f)
        print p
        if ".xml" in p:
            continue
        
if __name__=="__main__":
    auto_anno("../data")