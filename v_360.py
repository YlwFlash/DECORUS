import cv2
import numpy as np

def convert_to_360(video_capture):
    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture video.")
            break

        # Assuming a fisheye projection for the 360 effect
        height, width = frame.shape[:2]
        map_x, map_y = np.meshgrid(np.arange(width), np.arange(height))

        # Adjust the mapping for fisheye effect
        map_x = 2 * map_x / width - 1
        map_y = 2 * map_y / height - 1

        # Convert to polar coordinates
        r, theta = cv2.cartToPolar(map_x, map_y)

        # Apply fisheye distortion
        r = np.sqrt(r)
        r = np.clip(r, 0, 1)

        # Convert back to Cartesian coordinates
        map_x, map_y = cv2.polarToCart(r, theta)

        # Remap the frame using the fisheye mapping
        distorted_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        # Display the original and distorted frames
        cv2.imshow('Original', frame)
        cv2.imshow('360 Video', distorted_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 0 with the appropriate camera index or video file path
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Unable to open camera.")
    else:
        convert_to_360(video_capture)
