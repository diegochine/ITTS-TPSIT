from importlib import resources
from argparse import ArgumentParser, BooleanOptionalAction
import os
import cv2 as cv


def get_args():
    parser = ArgumentParser()

    parser.add_argument('-c', '--camera', action=BooleanOptionalAction, help='If set, uses camera')
    parser.add_argument('-i', '--input-dir', default=None, type=str,
                        help='Images input folder (must provide if not using camera)')
    parser.add_argument('-o', '--output-dir', default='out/', type=str,
                        help='Images output folder (must provide if not using camera)')

    return vars(parser.parse_args())


def detect_face(frame, detector, show=False):
    # convert to grayscale and "equalize" color
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    equalized_frame = cv.equalizeHist(gray_frame)

    # detect faces
    faces = detector.detectMultiScale(equalized_frame)
    print(f'Detected {len(faces)} faces')
    for (x, y, w, h) in faces:
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=5)
    if show:
        cv.imshow('Face detection', frame)
    return frame


def real_time_detection(detector):
    cam = cv.VideoCapture(0)  # id of the camera

    while True:
        _, frame = cam.read()
        detect_face(frame, detector, show=True)
        if cv.waitKey(30) > 0:
            break


if __name__ == '__main__':
    args = get_args()
    # create and load pretrained face classifier
    face_detector = cv.CascadeClassifier()
    pretrained_path = os.path.join(resources.path(package=cv, resource=''),
                                   'data\\haarcascade_frontalface_alt.xml')
    face_detector.load(pretrained_path)

    if args['camera']:
        real_time_detection(face_detector)
    else:
        assert args['input_dir'] is not None, 'Must provide input-dir if not using camera'
        if not os.path.isdir(args['output_dir']):
            os.makedirs(args['output_dir'])
        for imgname in os.listdir(args['input_dir']):
            in_path = os.path.join(args['input_dir'], imgname)
            out_path = os.path.join(args['output_dir'], imgname)
            img = cv.imread(in_path)
            processed = detect_face(img, face_detector)
            cv.imwrite(out_path, processed)

