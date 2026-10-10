
import cv2
import mediapipe as mp

# Initialize MediaPipe Face Landmarker
mp_face_mesh = mp.solutions.face_mesh

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    print("Face landmark detection started! Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read frame.")
            break

        # Mirror the webcam image
        frame = cv2.flip(frame, 1)

        # Convert BGR image to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect facial landmarks
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw facial landmark points
                for landmark in face_landmarks.landmark:
                    height, width, _ = frame.shape
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            cv2.putText(
                frame,
                "Face Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Facial Landmark Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
