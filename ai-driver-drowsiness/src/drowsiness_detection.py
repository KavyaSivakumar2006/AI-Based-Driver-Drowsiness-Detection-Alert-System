
import cv2
import mediapipe as mp
import math
import time

# Six landmark points around each eye
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Detection settings
EAR_THRESHOLD = 0.22
CLOSED_EYE_SECONDS = 1.5


def calculate_ear(eye_points):
    """Calculate the Eye Aspect Ratio (EAR)."""

    def distance(point_a, point_b):
        return math.dist(point_a, point_b)

    vertical_1 = distance(eye_points[1], eye_points[5])
    vertical_2 = distance(eye_points[2], eye_points[4])
    horizontal = distance(eye_points[0], eye_points[3])

    if horizontal == 0:
        return 0.0

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    mp_face_mesh = mp.solutions.face_mesh
    eyes_closed_since = None

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        print("Drowsiness detection started.")
        print("Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            status = "Face not detected"
            color = (0, 0, 255)

            if results.multi_face_landmarks:
                face = results.multi_face_landmarks[0]
                ear_values = []

                for eye_indices in [LEFT_EYE, RIGHT_EYE]:
                    points = []

                    for index in eye_indices:
                        landmark = face.landmark[index]
                        x = int(landmark.x * width)
                        y = int(landmark.y * height)
                        points.append((x, y))

                    ear = calculate_ear(points)
                    ear_values.append(ear)

                    # Display eye landmarks
                    for point in points:
                        cv2.circle(frame, point, 2, (0, 255, 0), -1)

                average_ear = sum(ear_values) / len(ear_values)

                cv2.putText(
                    frame,
                    f"EAR: {average_ear:.3f}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

                current_time = time.time()

                if average_ear < EAR_THRESHOLD:
                    if eyes_closed_since is None:
                        eyes_closed_since = current_time

                    closed_duration = current_time - eyes_closed_since

                    if closed_duration >= CLOSED_EYE_SECONDS:
                        status = "DROWSINESS WARNING!"
                        color = (0, 0, 255)
                    else:
                        status = "Eyes closed"
                        color = (0, 165, 255)
                else:
                    eyes_closed_since = None
                    status = "Awake"
                    color = (0, 255, 0)

            cv2.putText(
                frame,
                status,
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            cv2.imshow("Drowsiness Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
