import cv2
import numpy as np
import pyautogui
import keyboard
import mss
import mss.tools
import time

# Define the coordinates of the specific area to capture (adjust these values as per your requirement)
capture_area = {"left": 995, "top": 435, "width": 550, "height": 550}

# Take a screenshot of the specific area when F10 key is pressed
def take_screenshot():
    with mss.mss() as sct:
        screenshot = sct.grab(capture_area)
        screenshot = np.array(screenshot)
    return screenshot

# Start the white tile recognition and click automation
while True:
    if keyboard.is_pressed("F10"):
        # Take a screenshot
        screenshot = take_screenshot()

        # Convert the screenshot to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Threshold the grayscale image to obtain a binary mask for white tiles
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Find contours of white tiles in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the screenshot (for preview)
        cv2.drawContours(screenshot, contours, -1, (0, 255, 0), 2)

        # Display the screenshot with contours
        # cv2.imshow("Screenshot", screenshot)
        # cv2.waitKey(0)

        # Delay for 3 seconds
        time.sleep(3.5)

        # Iterate over the contours and click on each white tile
        for contour in contours:
            # Calculate the centroid of the contour
            moments = cv2.moments(contour)
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])

            time.sleep(.1)
            # Click on the centroid of the white tile
            pyautogui.click(capture_area["left"] + centroid_x, capture_area["top"] + centroid_y)

        # Wait for F10 key release to capture the next screenshot
        while keyboard.is_pressed("F10"):
            pass

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
