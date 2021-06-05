from pose_detect.pose_estimation import pose_main

import cv2, picamera

output_path = "./pose_images"

if __name__=='__main__':
    #camera = picamera.PiCamera(resolution=(640, 480), framerate=30)
    #preview = camera.start_preview()
    #preview.fullscreen = False
    #preview.window = (0, 0, 400, 400)
    #camera.start_preview()
    


    pose_main(output_path)

