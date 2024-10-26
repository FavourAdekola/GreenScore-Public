import cv2 as cv

capture = cv.VideoCapture(0)  # 0 is the default camera

while True:
    ret, frame = capture.read()  # Capture frame-by-frame
    if not ret:
        break
    
    cv.imshow('Video', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

capture.release()
cv.destroyAllWindows()