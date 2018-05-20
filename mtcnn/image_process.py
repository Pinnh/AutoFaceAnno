#encoding=utf-8
'''
Created on Sep 26, 2016

@author: pinnacle
'''

from PIL import Image, ImageOps,ImageChops
import numpy as np
import numbers
import random
import os 
import matplotlib.pyplot as plt
from skimage import exposure
import skimage.util as util
from PIL import ImageFilter
    

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
    
def resize_img(w_max, h_max, image,m_min=True):
    '''
    m_min if true then resized image max(width,height) is  w_max or h_max
          else then resized image min(width,height) is  w_max or h_max
    return image: PIL.Image,scale
    '''
    w=image.size[0]
    h=image.size[1]
    f1 = 1.0*w_max/w 
    f2 = 1.0*h_max/h
    factor = min([f1, f2]) if m_min else max([f1,f2])
    width = int(w*factor)
    height = int(h*factor)
    return image.resize((width, height), Image.ANTIALIAS),factor

def img_refull(w,h,img,mode='center',bg='white'):
    '''
    return images with fixed size that 
           content is paste from img but rescaled
    '''
    w1=img.size[0]
    h1=img.size[1]
    if w1>w or h1>h:
        print("refull fail")
        return img
    if bg=='white':
        rgbimg = Image.new("RGB",(w,h), (255, 255, 255))
    else:
        rgbimg = Image.new("RGB",(w,h))
    if mode=='center':
        rgbimg.paste(img,box=((w-w1)//2,(h-h1)//2))
    elif mode=='downright':
        rgbimg.paste(img,box=((w-w1),(h-h1)))
    elif mode=='random':
        top_=0 if w-w1==0 else np.random.randint(0,w-w1)
        left_=0 if h-h1==0 else np.random.randint(0,h-h1)
        rgbimg.paste(img,box=(top_,left_))
    else :
        rgbimg.paste(img)
    return rgbimg

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

class RandomCrop(object):

    def __init__(self, size, padding=0):
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.padding = padding

    def __call__(self, img):
        if self.padding > 0:
            img = ImageOps.expand(img, border=self.padding, fill=0)

        w, h = img.size
        th, tw = self.size
        if w == tw and h == th:
            return img

        x1 = random.randint(0, w - tw)
        y1 = random.randint(0, h - th)
        return img.crop((x1, y1, x1 + tw, y1 + th))
    
    
class ImageTransformer():
    
    def __init__(self,img_size=224):
        '''
        img_size: the image size that return
        '''
        self.rdcrop=RandomCrop(img_size)
        self.img_size=img_size
        
    def center_crop_img(self,img,rescaled_size=224):
        #img=img.resize((300,300))
        img,_=resize_img(224, 224,img,m_min=False)
        w, h = img.size
        th, tw = self.img_size,self.img_size
        x1 = int(round((w - tw) / 2.))
        y1 = int(round((h - th) / 2.))
        return img.crop((x1, y1, x1 + tw, y1 + th))
    
    def random_crop_img(self,img,rescaled_size=224):
        #img=img.resize((320,320))
        img,_=resize_img(rescaled_size,rescaled_size,img,m_min=False)
        img=self.rdcrop(img)
        return img
    
    def refull_img(self,img,mode='center',rescaled_size=224):
        '''
        mode: center downright topleft random
        '''
        #img=img.resize((320,320))
        img,_=resize_img(rescaled_size, rescaled_size,img,m_min=True)
        img=img_refull(self.img_size, self.img_size, img,mode=mode)
        return img
    
    def random_illumination(self,img,interval=(0.3,2)):
        seed=np.linspace(interval[0],interval[1],(interval[1]-interval[0])*10)
        illu=seed[np.random.randint(0,len(seed))]
        img= exposure.adjust_gamma(np.array(img),illu) 
        return Image.fromarray(img)
    
    def random_partial_illum(self,img,interval=(0.3,2)):
        seed=np.linspace(interval[0],interval[1],(interval[1]-interval[0])*10)
        illu=seed[np.random.randint(0,len(seed))]
        w,h=img.size[0],img.size[1]
        seed=np.random.randint(0,2)
        if seed==0:
            seed2=np.random.randint(0,w)
            im=img.crop(box=(seed2,0,w,h))
            im= exposure.adjust_gamma(np.array(im),illu) 
            im=Image.fromarray(im)
            img.paste(im,box=(seed2,0))
        else:
            seed2=np.random.randint(0,h)
            im=img.crop(box=(0,seed2,w,h))
            im= exposure.adjust_gamma(np.array(im),illu) 
            im=Image.fromarray(im)
            img.paste(im,box=(0,seed2))
        return img
    
    def to_gray(self,img):
        im=img_to_gray(img)
        return gray_to_rgb(im)
        
    def random_shadow(self,img):
        pass
    
    def random_filter(self,img):
        seed=np.random.randint(0,10)
        if seed==0:
            img = img.filter(ImageFilter.BLUR)
        #if seed==1:
        #    img = img.filter(ImageFilter.CONTOUR)
        if seed==2:
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        if seed==3:
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        #if seed==4:
        #    img = img.filter(ImageFilter.EMBOSS)
        #if seed==5:                    
        #    img = img.filter(ImageFilter.FIND_EDGES)  
        if seed==6:                                              
            img = img.filter(ImageFilter.SMOOTH)
        if seed==7:
            img = img.filter(ImageFilter.SMOOTH_MORE)
        if seed==8:
            img = img.filter(ImageFilter.SHARPEN)
        if seed==9:
            img = img.filter(ImageFilter.DETAIL)
        return img
    
    def random_contrast(self,img):
        start=np.random.randint(0,60)
        img=exposure.rescale_intensity(np.array(img),in_range=(start,255))
        return Image.fromarray(img)

    def random_rotate(self,img,degree=(0,365)):
        return img.rotate(np.random.randint(degree[0],degree[1]))
        
    def random_noise(self,img):
        seed=np.random.randint(3)
        img=np.array(img)
        if seed==0:
            im=util.random_noise(img)
        elif seed==1:
            im=util.random_noise(img,mode='s&p')
        else:
            im=util.random_noise(img,mode='poisson')
        return Image.fromarray(im,mode='RGB')
                
    def random_flip(self,img):
        seed=np.random.randint(3)
        if seed==0:
            im=img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            im=img.transpose(Image.FLIP_TOP_BOTTOM)
            
        return im
    
    def random_crop_side(self,img,padding=(20,20)):
        x=np.random.randint(0,padding[0])
        y=np.random.randint(0,padding[1])
        return img.crop(box=(x,y,img.size[0]-x,img.size[1]-y))
    
    def random_affine(self,img):
        pass
        #im=img.transform(img.size,Image.AFFINE,[1,0,rt1,0,1,rt2])
        #return im
        
    def random_offset(self,img):
        #img.offset()
        x=np.random.randint(0,10)
        y=np.random.randint(0,10)
        img=ImageChops.offset(img,x, y)
        return img
    
        
