import cv2, numpy as np
import matplotlib.pylab as plt


def cap_pix(_image):
    std_img = cv2.imread('/home/pi/raspi_alamy/image_processing/proc1/etc/co1.jpg')
    #cv2.imwrite("cann1.jpg", cv2.Canny(std_img, 50, 100))
    image = cv2.imread(_image)
    #cv2.imwrite("cann2.jpg", cv2.Canny(image, 50, 100))
    
    #img1= cv2.imread("cann1.jpg")
    #img2 = cv2.imread("cann2.jpg")
    img1 = cv2.imread('/home/pi/raspi_alamy/image_processing/proc1/etc/co1.jpg')
    img2 = cv2.imread(_image)
    
    cv2.imshow('query', img1)
    imgs = [img1, img2]
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
    
    ret = 0.68
    return ret

if __name__=='__main__':
    cap_pix('/tmp/sample_img.jpg')
