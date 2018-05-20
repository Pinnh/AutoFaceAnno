#encoding=utf-8
'''
Created on Sep 26, 2016

@author: pinnacle
'''

from PIL import Image, ImageOps,ImageChops
import numpy as np
import os 
import matplotlib.pyplot as plt
    

def show_img(data):
    plt.imshow(data)
    plt.show()
    
def image_to_3channels(raw_img_path,err_info=False):
    '''
    return PIL.Image if image is valid else None
    '''
    try:
        im=Image.open(raw_img_path)
        #im = im.resize((200,200), Image.ANTIALIAS)
        if len(np.shape(im))==3:
            if np.shape(im)[2]==3:#jpg
                return im
            elif np.shape(im)[2]>3:#png
                return png_to_rgb(im)
            else:
                return None
        elif len(np.shape(im))==2:#gray
            return gray_to_rgb(im)
        else:
            return None
        
    except Exception,e:
        if err_info:
            print e
        return None
    
def image_to_gray(raw_img_path,err_info=False):
    '''
    return PIL.Image if image is valid else None
    '''
    try:
        im=Image.open(raw_img_path)
        if len(np.shape(im))==3:
            return img_to_gray(im)
        elif len(np.shape(im))==2:#gray
            return im
        else:
            return None
    except Exception,e:
        if err_info:
            print e
        return None

def gray_to_rgb(img):
    rgbimg = Image.new("RGB", img.size)
    rgbimg.paste(img)
    return rgbimg

def png_to_rgb(img):
    rgbimg = Image.new("RGB", img.size, (255, 255, 255))
    rgbimg.paste(img, mask=img.split()[3])
    return rgbimg

def img_to_gray(img):
    return img.convert("L")

def image_to_str(img):
    imgstr=img.tobytes()
    return "%s,%s]%s"%(img.size[0],img.size[1],imgstr)
    
def str_to_image(imgstr):
    pos=imgstr.find("]")+1
    sarr=imgstr[:pos-1].split(",")
    return Image.frombytes("RGB",(int(sarr[0]),int(sarr[1])),imgstr[pos:])

def list_bad_images(xdir,show_info=True):
    bad_images=list()
    
    for i in os.listdir(xdir):
        p=os.path.join(xdir,i)
        if os.path.isdir(p):
            print '%s is a dir'%p
            continue
        try:
            Image.open(p).verify()
        except Exception,e:
            if show_info:
                print e
            bad_images.append(p)
            
    return bad_images

def save_image(img,file_path):
    img.save(file_path)
        
