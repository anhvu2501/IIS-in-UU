import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import re
from imageio import v3 as iio
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from tensorflow.keras import datasets, layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

gestures = ['ASL_letter_A','ASL_letter_B','ASL_letter_C','ASL_letter_L','ASL_letter_U','ASL_letter_R']

WIDTH = 256
HEIGHT = 256
CHANNELS = 3

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def coor_frames (condition):
    coor_videos = []
    path = (r"course_dataset/course_dataset/"+condition+"/videos/")
    videos = [f for f in listdir(path) if isfile(join(path, f))]
    videos.sort(key=natural_keys)
    for video in videos:
        if "(1)" not in video:
            frames = iio.imread(path+video)
            vid = []
            for frame in frames:
                frame = cv2.resize(frame,(256,256))
                vid = frame.apply(np.int64)
            coor_videos += [vid]
    return coor_videos


def coor_csv (condition):
  path = (r'course_dataset/'+ condition+ '/annotations.csv')
  ASL_train = pd.read_csv(path,
      names=["ID","frame", "gesture", "joint", "person_idx", "video_idx", "x", "y"])

  # Drop unneeded columns
  group_train = ASL_train.drop(['ID', 'gesture', 'joint', 'person_idx'], axis=1)

  # Group and re-index by person_idx and frame
  grouped_out = group_train.set_index(['video_idx', group_train.groupby(['video_idx']).cumcount()+1]).unstack().sort_index(level=1, axis=1)

  # Remove and reset the new indexes (Which were person_idx + frame)
  grouped_out.reset_index(drop=True, inplace=True)

  df = pd.DataFrame(grouped_out)
  df = df.to_numpy()

  return df[:-2]

def get_coordinates(condition):
    path_videos = (r"course_dataset/"+condition+"/videos/")
    path_csv = (r'course_dataset/'+condition+'/annotations.csv')
    coor_csv = []
    coor_videos = []
    ASL_train = pd.read_csv(path_csv,names=["ID", "frame", "gesture", "joint", "person_idx", "video_idx", "x", "y"])
    videos = [f for f in listdir(path_videos) if isfile(join(path_videos, f))]
    videos.sort(key=natural_keys)
    group_train = ASL_train.drop(['ID', 'gesture', 'joint', 'person_idx', 'video_idx'], axis=1)
    for video in videos:
        frames = iio.imread(path_videos+video)
        vid, df, grouped_out = [], [], []
        for frame in frames:
            frame = cv2.resize(frame, (256, 256))
            img = img_to_array(frame)
            vid += [img]
        vid_train = group_train[ASL_train["video_idx"]
                              == video.split('_')[1].split('.')[0]]

        grouped_out = vid_train.set_index(['frame', vid_train.groupby(
            ['frame']).cumcount()+1]).unstack().sort_index(level=1, axis=1)

        grouped_out.reset_index(drop=True, inplace=True)

        grouped_out.columns = grouped_out.columns.to_flat_index()

        df = pd.DataFrame(grouped_out)
        df = df.to_numpy()

        if len(df) < len(vid):
            break
        elif len(df) > len(vid):
            df = df[:-1]
        coor_csv += [df]
        coor_videos += vid
    flat_coor_csv = []
    for sublist in coor_csv:
        for item in sublist:
            item = [float(x) for x in item]
            flat_coor_csv.append(item)
    return coor_videos, flat_coor_csv



def createSimpleModel ():
    model = models.Sequential()
    model.add(layers.Conv2D(128, kernel_size=3, activation='relu', input_shape=(HEIGHT,WIDTH,CHANNELS)))
    model.add(layers.Dropout(0.5))
    model.add(layers.Conv2D(128, kernel_size=3, activation='relu'))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Conv2D(256, kernel_size=3, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Conv2D(256, kernel_size=3, activation='relu'))
    model.add(layers.MaxPooling2D((4,4)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Flatten())

    model.compile(optimizer="adam", loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def trainModel (model, x_train, y_train, x_test, y_test, epoch):
    model.fit(x_train, y_train, epochs=epoch, validation_data=(x_test, y_test))
    return model

total_X = []
total_y = []


#for condition in gestures:
X, y = get_coordinates("ASL_letter_A")

#total_X += [X]
#total_y += [y]

#print("total: ",total_y)


#X = np.array(X).astype('float64')
#y = np.array(y).astype('float64')
#X = X.tolist()
#y = y.tolist()
#X = np.array(X)
#y = np.array(y)


print("len x: ",len(X))
print("len y: ",len(y))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

print("data separated")

X_train = np.array(X_train).astype('float64')
y_train = np.array(y_train).astype('float64')
X_test = np.array(X_test).astype('float64')
y_test = np.array(y_test).astype('float64')

model = createSimpleModel()

print("model created")

print("start training")

trainModel(model,X_train,y_train,X_test,y_test,5)
