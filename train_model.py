import cv2
import numpy as np
import tensorflow
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from keras.applications import VGG16
from keras import models, layers, optimizers
from keras.models import Model
from keras.layers import Input, concatenate
from skimage.transform import resize

import os
import matplotlib.pyplot as plt
import pickle
import sklearn

import read_file_txt

def load_and_preprocess_data(label2id):
    X = []
    y = []

    for class_folder in os.listdir('./data/train'):
        class_path = os.path.join('./data/train', class_folder)

        for file_name in os.listdir(class_path):
            file_path = os.path.join(class_path, file_name)

            # Đọc ảnh và trích xuất đặc trưng SIFT
            img = cv2.imread(file_path)
            sift = cv2.SIFT_create()
            kp, des = sift.detectAndCompute(img, None)

            # Thêm đặc trưng SIFT và nhãn tương ứng vào danh sách
            X.append(kp)
            y.append(label2id[class_folder])

    return X, y

# Hàm chuyển đổi đặc trưng SIFT thành tensor hình ảnh

def sift_to_image(sift_features, image_size=(224, 224)):
    image = np.ones((image_size), dtype=np.uint8)
    keypoints = [cv2.KeyPoint(
                                x=feature.pt[0], 
                                y=feature.pt[1], 
                                _size=feature.size, 
                                _angle=feature.angle, 
                                _response=feature.response, 
                                _octave=feature.octave, 
                                _class_id=feature.class_id
                            ) for feature in sift_features]
    image = cv2.drawKeypoints(image, keypoints, image)
    return image


def main():

    # Load và chuyển đổi dữ liệu từ SIFT
    # X là danh sách các đặc trưng SIFT, y là nhãn tương ứng

    label2id = read_file_txt.read_file('./gesture_hand.txt')
    num_class = len(label2id)


    #label2id = {'like':0, 'loser':1, 'OK':2, 'punch':3, 'stop':4}
    X, y = load_and_preprocess_data(label2id)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Chuyển đổi đặc trưng SIFT thành tensor hình ảnh
    X_train_images = [sift_to_image(features) for features in X_train]
    X_test_images = [sift_to_image(features) for features in X_test]

    # Chuyển đổi nhãn thành dạng số
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    model_checkpoint = ModelCheckpoint(filepath='./model/save/saved_model.hdf5', save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_accuracy',
                                min_delta=0,
                                patience=15,
                                verbose=1,
                                mode='auto',
                                restore_best_weights=True)

    # Khởi tạo model
    model1 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    optimizer1 = optimizers.Adam()
    base_model = model1

    x = base_model.output
    x = Flatten()(x)
    x = Dense(128, activation='relu', name='fc1')(x)
    x = Dense(128, activation='relu', name='fc2')(x)
    x = Dense(128, activation='relu', name='fc2a')(x)
    x = Dense(128, activation='relu', name='fc3')(x)
    x = Dropout(0.5)(x)
    x = Dense(64, activation='relu', name='fc4')(x)

    predictions = Dense(num_class, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)


    # Biên soạn và huấn luyện mô hình
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(np.array(X_train_images), y_train_encoded, epochs=100, batch_size=32, validation_data=(np.array(X_test_images), y_test_encoded), callbacks=[early_stopping, model_checkpoint])


    model.save('./model/cnn_model_VGG16.hdf5')  #

    plt.figure(figsize=(12, 6))

    # Plot loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plot accuracy
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Hiển thị đồ thị
    plt.tight_layout()
    plt.show()
