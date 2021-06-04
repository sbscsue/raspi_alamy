from mkimg.cam import cap_img
from mkimg.set_img import canny_img
from cppixel.img_hist import cap_pix
from labeling.label_img import main_labeling

import argparse

label='remote control'
new_img='/tmp/sample_img.jpg'
std_img = "./etc/co1.jpg"

if __name__=='__main__':
    #parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--img', help='imge', required=True)
    #args = parser.parse_args()
    cap_img(std_img)
    #capter img

    #img_labeling
    
    label_str = main_labeling(new_img)
    print(label_str)
    if(label_str.find(label) != -1) :
        cap_pix(canny_img(new_img))
    
    print("include : " + str(label_str.find(label)))

    #img_compare_pixel
