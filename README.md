# Comp537-Project

This project aims to build an interface for facial expression editing. 

Initially, pre-trained model from STGAN [1] is used. You should clone the STGAN repository and place them under your current working directory. Then you should download the pre-trained model and place them under the ./output directory as described at https://github.com/csmliu/STGAN

For face recognition and image crop & align, imutils is used. Please install it by following the instructions at: https://github.com/jrosebr1/imutils



References: 
[1] M. Liu, Y. Ding, M. Xia, X. Liu, E. Ding, W. Zuo, and S. Wen, “STGAN: A Unified Selective Transfer Network for Arbitrary Image Attribute Editing,” in Proc. Conference on Computer Vision and Pattern Recognition, 2019.

[2] A.Rosebrock. "Face Alignment with OpenCV and Python". PyImageSearch. May 22, 2017. https://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/

