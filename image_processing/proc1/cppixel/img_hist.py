import cv2, numpy as np
import matplotlib.pylab as plt
from mkimg.set_img import canny_img


def cap_pix(_image):
    #std_img = cv2.imread('./etc/co1.jpg')
    std_img = canny_img('./etc/co1.jpg')
    image = cv2.imread(_image)
    #cv2.imshow('query', std_img)
    imgs = [std_img, image]
    hists=[]

    for i, img in enumerate(imgs) :
        plt.subplot(1, len(imgs), i+1)
        plt.title('img%d' % (i+1))
        plt.axis('off')
        plt.imshow(img[:,:,::-1])

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hist = cv2.calcHist([hsv], [0,1], None, [180, 256], [0, 180, 0, 2556])

        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

        hists.append(hist)


    query = hists[0]
    methods = {'CORREL' : cv2.HISTCMP_CORREL, 'CHISQR' : cv2.HISTCMP_CHISQR,
        'INTERSECT' : cv2.HISTCMP_INTERSECT, 'BHATTACHARYYA': cv2.HISTCMP_BHATTACHARYYA}

    for j, (name, flag) in enumerate(methods.items()):
        print('%-10s'%name, end='\t')
        for i, (hist, img) in enumerate(zip(hists, imgs)) :
            ret = cv2.compareHist(query, hist, flag)
            if flag == cv2.HISTCMP_INTERSECT :
                ret = ret/np.sum(query)
            print("img%d:%7.2f"%(i+1, ret), end = '\t')
        print()
    plt.show()
    
    print(ret)
    if(ret<0.5) : print("success!")

if __name__=='__main__':
    cap_pix('/tmp/sample_img.jpg')
