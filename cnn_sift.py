import copy
import cv2
import os
import time
import numpy as np
from keras.models import load_model
import time
from cvzone.HandTrackingModule import HandDetector

import read_file_txt


class _model():
    # Cac khai bao bien
    global model, score, gesture_names

    # Load model tu file da train
    model = load_model('./model/cnn_model_VGG16_19.hdf5')

    prediction = ''

    # gesture_names = {0: 'like',
    #                 1: 'loser',
    #                 2: 'OK',
    #                 3: 'punch',
    #                 4: 'stop'}

    label2id = read_file_txt.read_file('./gesture_hand.txt')
    gesture_names = {v: k for k, v in label2id.items()}

    # Ham de predict xem la ky tu gi
    def predict_rgb_image_vgg(self, image, model, gesture_names):

        image = np.array(image, dtype='float32')
        pred_array = model.predict(image)
        # print(f'pred_array: {pred_array}')

        result = gesture_names[np.argmax(pred_array)]
        # print(f'Result: {result}')
        # print(max(pred_array[0]))

        score = float("%0.2f" % (max(pred_array[0]) * 100))
        # print(result)

        return result, score

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        img = img.reshape((1, 224, 224, 3))
        return img

    def sift_to_image(self, sift_features, image_size=(224, 224)):
        image = np.zeros(image_size, dtype=np.uint8)
        #keypoints = [cv2.KeyPoint(x=feature[0], y=feature[1], _size=feature[2], _angle=feature[3], _response=feature[4], _octave=int(feature[5]), _class_id=int(feature[6])) for feature in sift_features]
        keypoints = [cv2.KeyPoint(x=feature.pt[0], y=feature.pt[1], _size=feature.size, _angle=feature.angle, _response=feature.response, _octave=feature.octave, _class_id=feature.class_id) for feature in sift_features]
        image = cv2.drawKeypoints(image, keypoints, image)
        return image


    def main_image(self, path):

        img = self.preprocess_image(path)

        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(img[0], None)

        img = self.sift_to_image(kp)

        img = np.expand_dims(img, axis=0)
        prediction, score = self.predict_rgb_image_vgg(img, model, gesture_names)

        return prediction

    def main_cam(self):
                    
        camera = cv2.VideoCapture(0)

        detector = HandDetector(detectionCon=0.8,maxHands=1)

        sift = cv2.SIFT_create()

        start_time = time.time()
        frames = 0

        while camera.isOpened():
            # Doc anh tu webcam
            ret, frame = camera.read()
            hands, frame = detector.findHands(frame, draw=False)

            # Tính thời gian từ khi bắt đầu và số khung hình
            frames += 1
            elapsed_time = time.time() - start_time

            # Tính FPS
            fps = frames / elapsed_time

            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if hands:
                x,y,w,h = hands[0]['bbox']
                fr = frame[y-20: (y+h)+30, x-20: (x+w)+30]
                if fr.size != 0:
                    cv2.imwrite('./hand_cut/hand_gesture.jpg',fr)
                cv2.rectangle(frame, (x-20,y-20), ( (x+w) + 30 , (y+h) + 30 ), (0,255,0), 3)
            
            if ret == True:
                
                file = './hand_cut'

                for i in os.listdir(file):
                    detect = os.path.join(file, i)
                    img = self.preprocess_image(detect)
                    
                    if hands:
                        
                        kp, des = sift.detectAndCompute(img[0], None)
                        img = self.sift_to_image(kp)
                        img = np.expand_dims(img, axis=0)
                        prediction, score = self.predict_rgb_image_vgg(img, model, gesture_names)
                        cv2.putText(frame,prediction, (50,50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break 


            cv2.imshow('original', frame)


        cv2.destroyAllWindows()
        camera.release()





