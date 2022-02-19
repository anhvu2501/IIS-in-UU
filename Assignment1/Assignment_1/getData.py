from os import listdir, read
from os.path import isfile, join
import re
import cv2
from imageio import v3 as iio
import mediapipe as mp
import numpy as np
import pandas as pd

# coor_csv = []
# path_csv = ('annotations.csv')
# data = pd.read_csv(path_csv)
# df = pd.DataFrame(data)
# df["coor"] = df['x'].astype(str) + ',' + df['y'].astype(str)
# # print(df)
# cols = [1,8]
# df = df[df.columns[cols]]
# # df = df.to_numpy()
# # # print(df[df_frame == 0])
# # print(df)
# # coor_csv += [df]
# # grouped = data.groupby('frame').groups.keys()
# df = df.groupby('frame')['coor'].apply(list).reset_index(name='coor')
# # df = df.to_numpy()
# print(df)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def coor_frames(condition):
    coor_videos = []
    path = (r"course_dataset/"+condition+"/videos/")
    videos = [f for f in listdir(path) if isfile(join(path, f))]
    videos.sort(key=natural_keys)
    for video in videos:
        frames = iio.imread(path+video)
        vid = []
        for frame in frames:
            frame = cv2.resize(frame, (256, 256))
            vid += [frame]
        coor_videos += [vid]
    return coor_videos


def get_coordinates(condition):
    path_videos = (r"course_dataset/"+condition+"/videos/")
    path_csv = (r'course_dataset/' + condition + '/annotations.csv')
    coor_csv = []
    coor_videos = []
    ASL_train = pd.read_csv(path_csv, names=[
                            "ID", "frame", "gesture", "joint", "person_idx", "video_idx", "x", "y"])
    videos = [f for f in listdir(path_videos) if isfile(join(path_videos, f))]
    videos.sort(key=natural_keys)
    group_train = ASL_train.drop(
        ['ID', 'gesture', 'joint', 'person_idx', 'video_idx'], axis=1)
    # df = pd.DataFrame()
    for video in videos:
        frames = iio.imread(path_videos+video)
        vid = []
        for frame in frames:
            frame = cv2.resize(frame, (256, 256))
            vid += [np.mean(frame)]
        coor_videos += vid
        vid_train = group_train[ASL_train["video_idx"]
                                == video.split('_')[1].split('.')[0]]

        # Group and re-index by person_idx and frame
        grouped_out = vid_train.set_index(['frame', vid_train.groupby(
            ['frame']).cumcount()+1]).unstack().sort_index(level=1, axis=1)

        # Remove and reset the new indexes (Which were person_idx + frame)
        grouped_out.reset_index(drop=True, inplace=True)

        grouped_out.columns = grouped_out.columns.to_flat_index()
        df = pd.DataFrame(grouped_out)
        df = df.to_numpy()
        coor_csv += [df]
        # print(grouped_out)
        # df = pd.DataFrame(grouped_out)
        # print(grouped_out)
    #     df = grouped_out
    # print(df)
    # coor_csv = df.to_numpy()
    # coor_csv.append(df)
        # print("processing video " + video.split('_')[1].split('.')[0] + " has len: ",len(df))
    # coor_csv.flatMap(lambda x: range(1, x)).collect()
    flat_coor_csv = []
    for sublist in coor_csv:
        for item in sublist:
            flat_coor_csv.append(item)
    return flat_coor_csv, coor_videos

# x = coor_frames('ASL_letter_A')
# print(len(x))


x, y = get_coordinates('ASL_letter_L')
print("len x: ", len(x))
print("len y: ", len(y))

# print(x)
# # print("************************")
# print("y: ")
# print(y[0], len(y[0]))

# read_videos('ASL_letter_A')
