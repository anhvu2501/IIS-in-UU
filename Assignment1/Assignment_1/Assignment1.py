import csv
import cv2
from imageio import v3 as iio

name = "ASL_letter_A"
frames = iio.imread(f"{name}.mp4")
x = 120
y = 120
i = 0
j = 0
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 0, 255)
    
for idx, frame in enumerate(frames):
    print(idx)
    with open('HO_VU_20010502-T018.csv', newline='') as f:
        reader = csv.reader(f)
        c = []
        for row in reader:
            #first row
            #print(row)
            if row[0] != "ID":
                r = int(float(row[2]))
            #print("r",r)
            if row[1] == name and r == idx:
                x = int(float(row[4]))
                y = int(float(row[5]))
                if x != 0:
                    cv2.circle(frame, (y, x), 5, color, 2)
                    c.append(row)
    last = "99"
    #print(c)
    if c[0][3] =="root":
        rx = int(float(c[0][4]))
        ry = int(float(c[0][5]))
    for circle in c:
        to_check = circle[3]
        #print(to_check)
        if to_check != 'root':
            finger = to_check.split("_")
            if finger[1] == '1':
                end_point = (int(float(circle[5])),int(float(circle[4])))
                cv2.line(frame, (ry,rx), end_point, color, 2)

            fingerindex = int(float(finger[1]))
            lastfingerindex = int(float(last[1]))
            
            offset = fingerindex - lastfingerindex
            if finger[0] == last[0] and offset == 1:                
                end_point = (int(float(circle[5])),int(float(circle[4])))
                start_point = (int(float(lastC[5])),int(float(lastC[4])))
                cv2.line(frame, start_point, end_point, color, 2)
                                         
            last = finger
            lastC = circle
        
    cv2.putText(frame, 'ANNOTATED', (1,50), font, 
                   1, color, 1, cv2.LINE_AA)
iio.imwrite(f"{name}_annotated.mp4", frames, fps=30)