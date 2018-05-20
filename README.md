AutoFaceAnno
========

Automatic face annotate by MTCNN(Pytorch,which you need install first).

Annotations are saved as XML files in PASCAL VOC format, the format used by ImageNet.

Thanks for the https://github.com/TropComplique/mtcnn-pytorch which use to detect faces in this project. 


Installation
------------------
Ubuntu Linux

Python 2

    sudo pip install lxml
    
    you can find pytorch instruction at https://pytorch.org/

Usage
------------------

     cd AutoFaceAnno/mtcnn
     PYTHONPATH=../ python auto_anno.py test ../data (for test)
     PYTHONPATH=../ python auto_anno.py anno ../data (for annotate)
     
Re-annotate
------------------
     You can use https://github.com/tzutalin/labelImg to modify the face rects and resave annotations.

     