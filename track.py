import cv2
import numpy as np
import time
from playsound import playsound
import csv
from multiprocessing import Process
from imports.logger import Logger
from imports.stats import StatsName, StatsColumns

# init part
face_cascade = cv2.CascadeClassifier('assets/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('assets/haarcascades/haarcascade_eye.xml')

def playBlinkSound():
    playsound('assets/sounds/blink.mp3')

def detect_faces(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        face_coords = [x, y, w, h]
        face_frame = img[y:y + h, x:x + w]
    return [
        face_coords,
        face_frame
    ]


def get_eyes_coords(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = [x,y,w,h]
        else:
            right_eye = [x,y,w,h]
    return left_eye, right_eye


def add_text_to_frame(frame, line, text):
    fontScale = 0.7
    position = (0, round(fontScale*30*(line+1)))
    color = (0, 255, 0)
    cv2.putText(frame, text, org=position, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=fontScale, color=color,thickness=1)


def add_infos_to_frame(frame, infos):
    for i in range(len(infos)):
        add_text_to_frame(frame, i, infos[i])

def nothing(x):
    pass


def main():
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    # log = csv.open()
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    # cv2.createTrackbar('threshold', 'image', 0, 255, nothing)



    time_started_at = time.time()
    time_elapsed = 0
    blink_count = 0
    is_blinking = False
    blink_per_minutes = 0

    logger = Logger(StatsColumns)
    logger.startLoggingData()

    while True:
        _, frame = cap.read()
        

        face = detect_faces(frame, face_cascade)
        if face is not None:
            face_coords, face_frame = face
            fx, fy, fw, fh = face_coords
            cv2.rectangle(frame,(fx,fy),(fx+fw,fy+fh),(0,0,255),2)

            eyes = get_eyes_coords(face_frame, eye_cascade)

            eye_lost_count = 0
            for eye in eyes:
                if eye is not None:
                    ex,ey,ew,eh = eye
                    cv2.rectangle(face_frame,(ex,ey),(ex+ew,ey+eh),(0,225,255),2)
                else:
                    eye_lost_count+=1
            
            if eye_lost_count==2 and not is_blinking:
                blink_count+=1
                is_blinking = True
                # p1 = Process(target=playBlinkSound)
                # p1.start()
            elif eye_lost_count==0:
                is_blinking = False

            time_elapsed = time.time() - time_started_at
            blink_per_minutes = (60*blink_count)/time_elapsed

        add_infos_to_frame(frame, [
            f'{StatsName.BLINK_COUNT}: {str(blink_count)}',
            f'{StatsName.IS_BLINKING}: {str(is_blinking)}',
            f'{StatsName.TIME_ELAPSED}: {str(round(time_elapsed, 1))}s',
            f'{StatsName.BLINK_PER_MINUTE}: {str(round(blink_per_minutes, 1))}',
        ])
        
        logger.updateData({
            StatsName.BLINK_COUNT: blink_count,
            StatsName.IS_BLINKING: is_blinking,
            StatsName.TIME_ELAPSED: time_elapsed,
            StatsName.BLINK_PER_MINUTE: blink_per_minutes,
        })

        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    logger.endLogging()

if __name__ == "__main__":
    main()
