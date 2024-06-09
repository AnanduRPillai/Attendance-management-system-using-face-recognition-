import face_recognition
import os
import cv2
import numpy as np
import math
import urllib.request


# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    students_present = []

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('image_folder'):
            face_image = face_recognition.load_image_file(f"image_folder/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    def run_recognition(self):
        my_list = []
        url='http://192.168.45.249/640x480.jpg'

        while True:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if self.process_current_frame:
                self.face_locations = face_recognition.face_locations(frame)
                self.face_encodings = face_recognition.face_encodings(frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])
                        print(f'{name} ({confidence})')
                        if float(confidence[:-1]) > 85.0:
                            my_list.append(name)
                            print(name)
                            if name not in self.students_present:
                                self.students_present.append(name)
                                print(self.students_present)

                    self.face_names.append(f'{name} ({confidence})')

            cv2.imshow('Face Recognition', frame)
            key = cv2.waitKey(5)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()
        return self.students_present


fr = FaceRecognition()
students_present = fr.run_recognition()
print("Students present:", students_present)