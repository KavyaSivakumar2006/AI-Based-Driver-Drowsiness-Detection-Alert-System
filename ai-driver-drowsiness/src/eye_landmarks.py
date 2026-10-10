
import cv2
import mediapipe as mp
import math


# Six landmark points around each eye
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


def calculate_ear(eye_points):
    """
    Calculate Eye Aspect Ratio (EAR) using six eye points.
    Lower EAR generally indicates a more closed eye.
    """

    def distance(point_a, point_b):
        return math.dist(point_a, point_b)

    # Vertical distances between upper and lower eyelids
    vertical_1 = distance(eye_points[1], eye_points[5])
    vertical_2 = distance(eye_points[2], eye_points[4])

    # Horizontal distance between eye corners
    horizontal = distance(eye_points[0], eye_points[3])

    if horizontal == 0:
        return 0.0

    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear


def main():
    mp_face_mesh = mp.solutions.face_mesh

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        print("Eye landmark and EAR detection started.")
        print("Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read webcam frame.")
                break

            # Mirror the webcam view
            frame = cv2.flip(frame, 1)

            height, width, _ = frame.shape

            # MediaPipe expects RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face in results.multi_face_landmarks:

                    for eye_name, eye_indices in [
                        ("Left", LEFT_EYE),
                        ("Right", RIGHT_EYE)
                    ]:
                        points = []

                        # Get the six eye landmark coordinates
                        for index in eye_indices:
                            landmark = face.landmark[index]

                            x = int(landmark.x * width)
                            y = int(landmark.y * height)

                            points.append((x, y))

                        # Draw eye landmarks and connect them
                        for i in range(6):
                            start = points[i]
                            end = points[(i + 1) % 6]

                            cv2.circle(
                                frame, start, 3, (0, 255, 0), -1
                            )

                            cv2.line(
                                frame, start, end, (255, 0, 0), 1
                            )

                        # Calculate EAR for this eye
                        ear = calculate_ear(points)

                        # Display EAR beside the eye
                        text_x = max(10, points[0][0] - 30)
                        text_y = max(25, points[0][1] - 15)

                        cv2.putText(
                            frame,
                            f"{eye_name} EAR: {ear:.3f}",
                            (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 255),
                            2
                        )

            else:
                cv2.putText(
                    frame,
                    "No face detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            cv2.imshow("Eye Landmark and EAR Detection", frame)

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
