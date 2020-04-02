
import cv2

def modif(img_path):
    img=cv2.imread(img_path+"img0.jpg")
    img[:,:,2]=0
    cv2.imwrite(img_path+"img0_bw.jpg", img)
    return img_path+"img0_bw.jpg"