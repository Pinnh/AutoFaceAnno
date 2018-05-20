import sys
sys.path.insert(0, "path_to_caffe/caffe-master/build/install/python")
import caffe
import numpy as np
import torch
from torch.autograd import Variable
from get_nets import PNet, RNet, ONet
import cv2
"""
The purpose of this script is to convert pretrained weights taken from
official implementation here:
https://github.com/kpzhang93/MTCNN_face_detection_alignment/tree/master/code/codes/MTCNNv2
to required format.

In a nutshell, it just renames and transposes some of the weights.
You don't have to use this script because weights are already in `src/weights`.
"""


def get_all_weights(net):
    all_weights = {}
    for p in net.params:
        if 'conv' in p:
            name = 'features.' + p
            if '-' in p:
                s = list(p)
                s[-2] = '_'
                s = ''.join(s)
                all_weights[s + '.weight'] = net.params[p][0].data
                all_weights[s + '.bias'] = net.params[p][1].data
            elif len(net.params[p][0].data.shape) == 4:
                all_weights[name + '.weight'] = net.params[p][0].data.transpose((0, 1, 3, 2))
                all_weights[name + '.bias'] = net.params[p][1].data
            else:
                all_weights[name + '.weight'] = net.params[p][0].data
                all_weights[name + '.bias'] = net.params[p][1].data
        elif 'prelu' in p.lower():
            all_weights['features.' + p.lower() + '.weight'] = net.params[p][0].data
    return all_weights

def save_to_pytorch():
    #P-Net
    net = caffe.Net('caffe_models/det1.prototxt', 'caffe_models/det1.caffemodel', caffe.TEST)
    np.save('src/weights/pnet.npy', get_all_weights(net))
     
    # R-Net
    net = caffe.Net('caffe_models/det2.prototxt', 'caffe_models/det2.caffemodel', caffe.TEST)
    np.save('src/weights/rnet.npy', get_all_weights(net))
     
    # O-Net
    net = caffe.Net('caffe_models/det3.prototxt', 'caffe_models/det3.caffemodel', caffe.TEST)
    np.save('src/weights/onet.npy', get_all_weights(net))


def torch_to_caffe_pnet():
    net = caffe.Net('../caffe_models/det1.prototxt', '../caffe_models/det1.caffemodel', caffe.TEST)
    pm=torch.load("../model/pnet.pm")
    for k in net.params:
        print k,np.shape(net.params[k][0].data)
    for k,v in pm.items():
        v=pm[k].numpy()
        print k,np.shape(v)
        k=k.replace("features.","").replace("_",'-')
        if ".weight" in k:
            kc=k.replace(".weight","")
            if 'prelu' in kc:
                kc=kc.replace("prelu","PReLU")
            if len(np.shape(v))==4:
                net.params[kc][0].data[...]=v.transpose((0, 1, 3, 2))
            else:
                net.params[kc][0].data[...]=v
        elif ".bias" in k:
            kc=k.replace(".bias","")
            net.params[kc][1].data[...]=v
    net.save('../model/det1_new.caffemodel')
    
            
def torch_to_caffe_rnet():
    net = caffe.Net('../caffe_models/det2.prototxt', '../caffe_models/det2.caffemodel', caffe.TEST)
    for k in net.params:
        print k,np.shape(net.params[k][0].data)
    
    #rnet=RNet()
    #pm=rnet.state_dict()
    pm=torch.load("../model/rnet.pm")
    for k,v in pm.items():
        v=pm[k].numpy()
        print k,np.shape(v)
        k=k.replace("features.","").replace("_",'-')
        if ".weight" in k:
            kc=k.replace(".weight","")
            if len(np.shape(v))==4:
                net.params[kc][0].data[...]=v.transpose((0, 1, 3, 2))
            else:
                net.params[kc][0].data[...]=v
        elif ".bias" in k:
            kc=k.replace(".bias","")
            net.params[kc][1].data[...]=v
    net.save('../model/det2_new.caffemodel')        
            
if __name__=="__main__":
    torch_to_caffe_pnet()
    torch_to_caffe_rnet()

    
    
    