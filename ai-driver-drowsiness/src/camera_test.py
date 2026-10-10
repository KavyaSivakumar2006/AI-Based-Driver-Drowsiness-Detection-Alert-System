
import cv2

# Open the default webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam started! Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Error: Could not read frame.")
        break

    cv2.imshow("Driver Drowsiness Detection - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
