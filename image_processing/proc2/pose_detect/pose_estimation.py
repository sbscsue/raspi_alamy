#import packages
import os, argparse, cv2
import numpy as np
import time, random
import pathlib, datetime, time
from threading import Thread
from tflite_runtime.interpreter import Interpreter
from .keypoint import keypoint

default_model = "/home/pi/Documents/ex_project/ex/image_processing/proc2/etc/default.tflite"

class VideoStream:
    def __init__(self, resolution = (640, 480), framerate = 30):

        self.stream = cv2.VideoCapture(0)
        print("Camera initiated.")
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        ret = self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        (self.status, self.frame) = self.stream.read()
        self.stopped = False    
        self.nonce = make_nonce(resolution)
        self.per_w = [0]*2
        self.per_h = [0]*2
        self.per_w[0] = self.nonce[0]/resolution[0]
        self.per_w[1] = (self.nonce[0]+200)/resolution[0]

        self.per_h[0] = self.nonce[1]/resolution[1]
        self.per_h[1] = (self.nonce[1]+200)/resolution[1]


        print("keypoint : %d, offset : (%d, %d) - (%.2f ~ %.2f, %.2f ~ %.2f)" % (self.nonce[2], self.nonce[0], self.nonce[1], self.per_w[0], self.per_w[1], self.per_h[0], self.per_h[1]))

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return
            (self.status, self.frame) = self.stream.read()
            self.cap = self.frame.copy()
            if self.status :
                cv2.rectangle(self.cap, (self.nonce[0], self.nonce[1]),(self.nonce[0]+200, self.nonce[1]+200), (255, 0, 0), 5)
                cv2.putText(self.cap, keypoint[self.nonce[2]], (320, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.imshow("label", self.cap)
                if cv2.waitKey(1)&0xFF == ord('q'):
                    break 
        cap.release()

    def read_f(self):
        return self.frame

    def stop(self):
        self.stopped = True

#parser = argparse.ArgumentParser()
#parser.add_argument('--modeldir', help = 'Folder the .tflite file is located in')
#parser.add_argument('--model', help = 'Name of the .tflite file, if different than detect.tflite', required=True)
#parser.add_argument('--threshold', help='Threshold for displaying detected keypoints (between 0 and 1).', default = 0.5)
default_threshold=0.5
default_resolution = '640x480'
#parser.add_argument('--resolution', help='Desired webcam resolution in WxH.', default = '640x480')
#parser.add_argument('--output_path', help='Where to save processed images from pi.', required=True)

#args = parser.parse_args()
#MODELDIR_NAME = args.modeldir
MODEL_NAME = default_model
min_conf_threshold = float(default_threshold)
#resW, resH = args.resolution.split('x')
resW, resH = default_resolution.split('x')
imW, imH = int(resW), int(resH)

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME)
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

output_stride = 32
floating_model = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5

#cv2.namedWindow('Result')

def mod(a,b):
    floored = np.floor_divide(a,b)
    return np.subtract(a, np.multiply(floored, b))

def sigmoid(x) :
    return 1/(1+np.exp(-x))

def sigmoid_and_argmax2d(inputs, threshold) :
    v1 = interpreter.get_tensor(output_details[0]['index'])[0]
    height = v1.shape[0]
    width = v1.shape[1]
    depth = v1.shape[2]
    reshaped = np.reshape(v1, [height * width, depth])
    reshaped = sigmoid(reshaped)

    reshaped = (reshaped > threshold) * reshaped

    coords = np.argmax(reshaped, axis=0)
    yCoords = np.round(np.expand_dims(np.divide(coords, width), 1))
    xCoords = np.expand_dims(mod(coords, width), 1)
    return np.concatenate([yCoords, xCoords], 1)

def get_offset_point(y,x,offsets,keypoint,num_key_points):
    y_off = offsets[y,x,keypoint]
    x_off = offsets[y,x,keypoint+num_key_points]
    return np.array([y_off, x_off])

def get_offsets(output_details, coords, num_key_points=17):
    offsets = interpreter.get_tensor(output_details[1]['index'])[0]
    offset_vectors = np.array([]).reshape(-1, 2)
    for i in range(len(coords)):
        heatmap_y = int(coords[i][0])
        heatmap_x = int(coords[i][1])

        if heatmap_y >8 :
            heatmap_y = heatmap_y -1
        if heatmap_x >8 :
            heatmap_x = heatmap_x -1
        offset_vectors = np.vstack((offset_vectors, get_offset_point(heatmap_y, heatmap_x, offsets, i, num_key_points)))
    return offset_vectors

def draw_lines(keypoints, image, bad_pts):
    color = (0, 255, 0)
    thickness = 2
    body_map = [[5,6],[5,7],[7,9],[5,11],[6,8],[8,10],[6,12],[11,12],[11,13],[13,15],[12,14],[14,16]]
    for map_pair in body_map:
        if map_pair[0] in bad_pts or map_pair[1] in bad_pts:
            continue
        start_pos = (int(keypoints[map_pair[0]][1]), int(keypoints[map_pair[0]][0]))
        end_pos = (int(keypoints[map_pair[1]][1]), int(keypoints[map_pair[1]][0]))
        image = cv2.line(image, start_pos, end_pos, color, thickness)
    return image

def make_nonce(_res):
    # rand num for rectangle
    nonce1 = random.randrange(5, _res[0]-200)
    nonce2 = random.randrange(5, _res[1]-200)
    # rand num for rand key points
    nonce_num = random.randrange(0, 9)

    return (nonce1, nonce2, nonce_num)
    

def pose_main(_path):
    debug = True

    try:
        outdir = pathlib.Path(_path) / time.strftime('%Y-%m-%d_%H-%M-%S-%Z')
        outdir.mkdir(parents = True)
        time.sleep(0.1)
        f = []

        frame_rate_clac = 1
        freq = cv2.getTickFrequency()
        videostream = VideoStream(resolution = (imW, imH), framerate=30).start()
        time.sleep(1)

        while True:
            print('running loop')
            t1 = cv2.getTickCount()
            frame1 = videostream.read_f()
            frame = frame1.copy()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)
            frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            coords = sigmoid_and_argmax2d(output_details, min_conf_threshold)
            drop_pts = list(np.unique(np.where(coords == 0)[0]))

            offset_vectors = get_offsets(output_details, coords)
            keypoint_positions = coords * output_stride + offset_vectors

            #if debug :
                #print(keypoint_positions)
            for i in range(len(keypoint_positions)):
                if i in drop_pts:
                    continue
                x = int(keypoint_positions[i][1])
                y = int(keypoint_positions[i][0])
                center_coordinates=(x,y)
                radius = 2
                color = (0, 255, 0)
                thickness = 2
                cv2.circle(frame_resized, center_coordinates, radius, color, thickness)
                per= [0]*2
                per[0] = center_coordinates[0]/int(width)
                per[1] = center_coordinates[1]/int(height)

                print("key point : %d,  offset : (%.2f, %.2f)" %(i, per[0], per[1]))
                if(i==videostream.nonce[2]):
                    if(per[0]>videostream.per_w[0] and per[0]<videostream.per_w[1] and per[1]>videostream.per_h[0] and per[1]<videostream.per_h[1]):
                        print("suucesss!!!!!!\n\n\n\n")
                        videostream.stop() 
                        cv2.destroyAllWindows()
                        #videostream.stop()
                        return True
                if debug:
                    cv2.putText(frame_resized, str(i), (x-4, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
                    frame_resized = draw_lines(keypoint_positions, frame_resized, drop_pts)
                    t2 = cv2.getTickCount()
                    time1 = (t2-t1)/freq
                    frame_rate_clac = 1/time1
                    f.append(frame_rate_clac)
                    path = str(outdir) + '/' + str(datetime.datetime.now()).replace(" ", "_") + ".jpg"
                    status = cv2.imwrite(path, frame_resized)
                    cv2.imshow('Result', frame_resized)
                
                    if cv2.waitKey(10) == ord('q'):
                        print(f"Saved images to: {outdir}")
                        cv2.destroyAllWindows()
                        videostream.stop()
                        time.sleep(2)
                        break

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        videostream.stop()
        print('Stopped video stream.')


