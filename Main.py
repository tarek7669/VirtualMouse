import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

thumb_x = 0
thumb_y = 0

index_x = 0
index_y = 0
index_bottom_x = 0
index_bottom_y = 0

middle_x = 0
middle_y = 0
middle_bottom_x = 0
middle_bottom_y = 0

ring_x = 0
ring_y = 0
ring_bottom_x = 0
ring_bottom_y = 0

pinky_x = 0
pinky_y = 0

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # print(x, y)
                if id == 8: # the landmark of the index finger
                    cv2.circle(img = frame, center=(x,y), radius = 15, color = (255,255,255))
                    index_x = screen_width/frame_width * x
                    index_y = screen_height/frame_height * y

                if id == 4: # the landmark of the thumb finger
                    cv2.circle(img = frame, center=(x,y), radius = 15, color = (255,255,255))
                    thumb_x = screen_width/frame_width * x
                    thumb_y = screen_height/frame_height * y
                    # print(abs(index_y - thumb_y))

                    # if abs(index_y - thumb_y) < 50:
                    #     pyautogui.click()
                    #     pyautogui.sleep(1)
                    #     print("clicked")

                if id == 12: # the landmark of the middle finger
                    cv2.circle(img = frame, center=(x,y), radius = 15, color = (0,0,0))
                    middle_x = screen_width/frame_width * x
                    middle_y = screen_height/frame_height * y
                    pyautogui.moveTo(middle_x,middle_y)


                    # one left mouse click
                    # if(abs(index_x - middle_x) < 80 and abs(ring_x - middle_x) < 80):
                    #     pyautogui.click()
                    #     pyautogui.sleep(1)
                    #     print("clicked")


                if id == 16: # the landmark of the ring finger
                    cv2.circle(img = frame, center=(x,y), radius = 15, color = (255,255,255))
                    ring_x = screen_width/frame_width * x
                    ring_y = screen_height/frame_height * y


                if id == 20: # the landmark of the pinky finger
                    cv2.circle(img = frame, center=(x,y), radius = 15, color = (255,255,255))
                    pinky_x = screen_width/frame_width * x
                    pinky_y = screen_height/frame_height * y


                if id == 9: # the landmark of the bottom of the middle finger (for the screenshot)
                    middle_bottom_x = screen_width/frame_width * x
                    middle_bottom_y = screen_height/frame_height * y

                    if(abs(middle_bottom_x - thumb_x) < 50 and abs(middle_bottom_x - pinky_x) < 50):
                        pyautogui.hotkey('win','prtsc')


                if id == 5: # the landmark of the bottom of the index finger (for mouse click)
                    index_bottom_x = screen_width/frame_width * x
                    index_bottom_y = screen_height/frame_height * y

                if id == 13: # the landmark of the bottom of the ring finger (for mouse click)
                    ring_bottom_x = screen_width/frame_width * x
                    ring_bottom_y = screen_height/frame_height * y

                    if(abs(index_bottom_y - index_y) > 20 and abs(ring_bottom_y - ring_y)
                    and abs(index_x - middle_x) < 80 and abs(ring_x - middle_x) < 80):
                        pyautogui.click()
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)