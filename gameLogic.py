import cv2
import os


fireball = ['Horse','Serpent','Ram','Monkey','Boar','Horse','Tiger']
userInput = []
counter =0



# Yolo class name put into the user array
for i in range(len(fireball)):
    while True:
        handsign = input("what is the hand sign")
        if i== 0 or handsign!= userInput[-1]:
            userInput.append(handsign)
            break
        else:
            print("Wrong sign!")


print(userInput)
# check each array to see if inputs equals an input
for i in range(len(fireball)):
    if fireball[i] == userInput[i]:
        counter += 1
        if counter == 7:

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

            # Step 4: Release resources and clean up
            cap.release()
            cv2.destroyAllWindows()
            print("Video playback completed.")