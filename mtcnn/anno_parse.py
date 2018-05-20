'''
Created on May 20, 2018

@author: pinnacle
'''
import os
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 
import xml.dom.minidom as minidom
import numpy as np

def xml_anno_parse(xml_file):
    '''
    '''
    try: 
        annotation_map=dict()
        tree = ET.parse(xml_file) 
        root = tree.getroot()
        filename=root.find("filename").text
        segmented=root.find("segmented").text
        size_node=root.find("size")
        width=size_node.find("width").text
        height=size_node.find("height").text
        depth=size_node.find("depth").text
        annotation_map["filename"]=filename
        #image size
        annotation_map["size"]=[int(width),int(height),int(depth)]
        #for segment task if 1
        annotation_map["segmented"]=int(segmented)
        objs=list()
        for onode in root.findall("object"):
            obj_map=dict()
            name=onode.find("name").text
            pose=onode.find("pose").text
            truncated=onode.find("truncated").text
            difficult=onode.find("difficult").text
            boundbox_node=onode.find("bndbox")
            xmin=boundbox_node.find("xmin").text
            ymin=boundbox_node.find("ymin").text
            xmax=boundbox_node.find("xmax").text
            ymax=boundbox_node.find("ymax").text
            obj_map["name"]=name
            obj_map["pose"]=pose
            obj_map["truncated"]=truncated
            obj_map["difficult"]=difficult
            obj_map["box"]=[int(xmin),int(ymin),int(xmax),int(ymax)]
            objs.append(obj_map)
            annotation_map["objs"]=objs
        return annotation_map
    except Exception, e: 
        print e

def save_anno_to_xml(file_path,width,height,depth,annos):
    root_tag="annotation"
    root_name = ET.Element(root_tag)
    folder = ET.SubElement(root_name,"folder")
    folder.text="Unknown"
    filename = ET.SubElement(root_name,"filename")
    filename.text=os.path.basename(file_path)
    path = ET.SubElement(root_name,"path")
    path.text=file_path
    source = ET.SubElement(root_name,"source")
    database = ET.SubElement(source, "database")
    database.text="Unknown"
    
    size = ET.SubElement(root_name,"size")
    width_node = ET.SubElement(size, "width")
    height_node = ET.SubElement(size, "height")
    depth_node = ET.SubElement(size, "depth")
    width_node.text=str(width)
    height_node.text=str(height)
    depth_node.text=str(depth)
    
    segmented = ET.SubElement(root_name,"segmented")
    segmented.text="0"
    
    for index,anno in enumerate(annos):
        print "anno:",anno
        xmin,ymin,xmax,ymax=np.asarray(anno,np.int)
        obj = ET.SubElement(root_name,"object")
        name = ET.SubElement(obj,"name")
        name.text=str(index)
        pose = ET.SubElement(obj,"pose")
        pose.text="Unspecified"
        truncated = ET.SubElement(obj,"truncated")
        truncated.text="0"
        difficult = ET.SubElement(obj,"difficult")
        difficult.text="0"
        bndbox = ET.SubElement(obj,"bndbox")
        xmin_node = ET.SubElement(bndbox,"xmin")
        xmin_node.text=str(xmin)
        ymin_node = ET.SubElement(bndbox,"ymin")
        ymin_node.text=str(ymin)
        xmax_node = ET.SubElement(bndbox,"xmax")
        xmax_node.text=str(xmax)
        ymax_node = ET.SubElement(bndbox,"ymax")
        ymax_node.text=str(ymax)
        
    #tree = ET.ElementTree(root_name)
    dir_name=os.path.dirname(file_path)
    file_name=os.path.basename(file_path)
    #tree.write(os.path.join(dir_name,file_name.split(".")[0]+".xml"), encoding='utf-8')
    rough_string = ET.tostring(root_name, 'utf-8')
    reared_content = minidom.parseString(rough_string)
    with open(os.path.join(dir_name,file_name.split(".")[0]+".xml"), 'w+') as fs:
        reared_content.writexml(fs, addindent=" ", newl="\n", encoding="utf-8")

    
    