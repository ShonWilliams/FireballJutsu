import cv2
from ultralytics import YOLO

# Define the sequence of gestures for the "fireball"
fireball = ['Horse', 'Serpent', 'Ram', 'Monkey', 'Boar', 'Horse', 'Tiger']
userInput = []  # Stores the user's input gestures
counter = 0  # Tracks the position in the fireball sequence
last_detected_gesture = None  # Tracks the last detected gesture to avoid duplicates

# Load the YOLO model once (outside the loop)
model = YOLO('best(2).pt')

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break  # Exit if the frame is not captured

    # Run YOLOv8 tracking on the frame
    results = model.track(frame, persist=True)

    # Get the result details: boxes, labels, and confidences
    boxes = results[0].boxes.xyxy  # Bounding box coordinates (x1, y1, x2, y2)
    labels = results[0].boxes.cls  # Class labels
    confidences = results[0].boxes.conf  # Confidence scores

    # Process each detected object
    for i in range(len(boxes)):
        # Extract the coordinates, class label, and confidence for each detected object
        x1, y1, x2, y2 = boxes[i].tolist()
        label = int(labels[i].item())
        confidence = confidences[i].item()
        class_name = model.names[label]  # Retrieve class name using the label index

        # Print all detected class names and confidence scores
        print(f"Detected: {class_name} (Confidence: {confidence:.2f})")

        # Filter out low-confidence detections
        if confidence > 0.7:  # Adjust the threshold as needed
            # Check if the detected gesture is new (not the same as the last detected gesture)
            if class_name != last_detected_gesture:
                last_detected_gesture = class_name  # Update the last detected gesture
                print(f"New gesture detected: {class_name}")

                # Check if the detected gesture matches the expected gesture in the sequence
                if counter < len(fireball) and class_name == fireball[counter]:
                    userInput.append(class_name)
                    counter += 1  # Move to the next gesture in the sequence
                    print(f"Correct gesture detected: {class_name}")
                    print(f"User input so far: {userInput}")

                    # Check if the user has completed the sequence
                    if counter == len(fireball):
                        # Full path to the video file
                        video_path = r"C:\Users\Shon Williams\PycharmProjects\NarutoHandSigns\Fireball Jutsu.avi.mp4"

                        # Step 2: Open the video file
                        cap = cv2.VideoCapture(video_path)

                        # Get video FPS (frames per second)
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        # Calculate delay in milliseconds
                        delay = int(1000 / fps)

                        # Make window full screen and stay on top
                        cv2.namedWindow('Fireball Jutsu', cv2.WINDOW_FULLSCREEN)
                        cv2.setWindowProperty('Fireball Jutsu', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                        # Step 3: Playback the video
                        while True:
                            ret, frame = cap.read()
                            if not ret:  # End of video or failed to read a frame
                                print("End of video or failed to retrieve frames.")
                                break

                            # Show the video frame
                            cv2.imshow('Fireball Jutsu', frame)

                            # Quit on pressing 'q'
                            if cv2.waitKey(delay) & 0xFF == ord('q'):
                                print("Exiting video playback.")
                                break
                        #userInput = []  # Reset for the next sequence
                        #counter = 0
                else:
                    print("Wrong gesture! Resetting...")
                    userInput = []  # Reset if the wrong gesture is detected
                    counter = 0

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name}: {confidence:.2f}",
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking and Hand Gestures", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()