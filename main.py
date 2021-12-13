import cv2
import mediapipe as mp
import win32api, win32con
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0) #Kamera ID
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    height, width, channels = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        #Hole Zeigefingerkuppe Koordinaten und rechne diese in Pixel  um
        indextipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
        indextipY = height - (height * hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) #Spiegle Y von oben zu unten auf unten nach oben
        indexstring = 'index: ' + str(indextipX)[:3] + " : " + str(indextipY)[:4] #Setze Ausgabe zusammen
        #Hole Daumenkuppe Koordinaten und reche diese in Pixel um
        thumbtipX = (width * hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
        thumbtipY = height - (height * hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)#Spiegle Y von oben zu unten auf unten nach oben
        thumbstring = 'Thumb: ' + str(thumbtipX)[:3] + " : " + str(thumbtipY)[:4]
        distanceX = abs(indextipX - thumbtipX)
        distanceY = abs(indextipY - thumbtipY)

        distancestring = 'Distance: ' + str(distanceX)[:3] + " : " + str(distanceY)[:4]
        cv2.flip(image, 1)
        if distanceX <= 20 and distanceY <= 20:
            distanceColor = (0,0,255)
            win32api.SetCursorPos((int(thumbtipX), int(thumbtipY)))
        else: distanceColor = (255,255,255)

        image = cv2.putText(image, indexstring[:], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        image = cv2.putText(image, thumbstring[:], (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,cv2.LINE_AA)
        image = cv2.putText(image, distancestring[:], (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, distanceColor, 2,cv2.LINE_AA)
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.


    cv2.imshow('Anwendung für freihändige Eingabe', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()