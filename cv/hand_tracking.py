import cv2 as cv
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self.max_hands = max_hands
        self.detectionCon = detection_conf
        self.trackCon = track_conf
        self.hands = mp.solutions.hands.Hands(False, self.max_hands,
                                              min_detection_confidence=self.detectionCon,
                                              min_tracking_confidence=self.trackCon)

    def find_hands(self, img, draw=True):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)    # converting from BGR to RGB
        self.results = self.hands.process(img_rgb)      # mediapipe processing of the RGB image
        if self.results.multi_hand_landmarks and draw:  # if hands detected (and want to draw)
            for handLms in self.results.multi_hand_landmarks:  # each hand landmarks is a triple (x, y, z)
                mp.solutions.drawing_utils.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)
        print(f'Detected {len(self.results.multi_hand_landmarks)} hands')
        return img

    def add_bbox(self, img, hand=0, draw=True):
        xs = []
        ys = []
        bbox = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand]
            for id, lm in enumerate(myHand.landmark):  # gives id and lm(x,y,z)
                h, w, c = img.shape  # getting h, w for converting decimals x, y into pixels
                cx, cy = int(lm.x * w), int(lm.y * h)  # pixels coordinates for landmarks
                xs.append(cx)
                ys.append(cy)
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 0, 255), cv.FILLED)
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

        return bbox


if __name__ == "__main__":
    prev_time = 0
    cam = cv.VideoCapture(0)
    detector = HandDetector()

    while True:
        _, img = cam.read()
        img = detector.find_hands(img)
        lmlist, bbox = detector.add_bbox(img)

        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time
        cv.putText(img, f'{int(fps)}', (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)  # showing Fps on screen

        cv.imshow("Hand tracking demo", img)
        cv.waitKey(10)
