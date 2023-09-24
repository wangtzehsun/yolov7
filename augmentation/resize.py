import cv2
import os

# Load the image
image = cv2.imread('F:/ESCI/yolov7/augmentation/basketdata/raw_images/abc.jpg')

# Check if the image was loaded successfully
if image is not None:
    # Define the target size (640x640 in this case)
    target_size = (640, 640)

    # Resize the image
    resized_image = cv2.resize(image, target_size)

    # Specify the output file path (absolute or relative)
    output_path = 'F:/ESCI/yolov7/augmentation/basketdata/raw_images/resized_image.jpg'

    # Save the resized image
    cv2.imwrite(output_path, resized_image)
    print("Resized image saved successfully.")
else:
    print("Failed to load the input image.")
