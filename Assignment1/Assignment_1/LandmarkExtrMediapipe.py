import cv2
import mediapipe as mp


capture = cv2.VideoCapture('course_dataset/ASL_letter_A/videos/video_0.mp4')

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
   
size = (frame_width, frame_height)

while True:
    success, frame = capture.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    # print(results.multi_hand_landmarks)

    coor = []
    joint = [(0,0)]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Video", frame)
    if cv2.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv2.destroyAllWindows()
