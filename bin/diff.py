import cv2
import numpy as np

def create_test_images():
    image1 = np.zeros((100, 100, 3), np.uint8)
    image1[:] = (0, 0, 255)  # Red image

    image2 = np.copy(image1)
    cv2.circle(image2, (50, 50), 20, (0, 255, 0), -1)  # Green spot in the middle

    return image1, image2

def find_differences(image1, image2):
    diff = cv2.absdiff(image1, image2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # Create an image to hold only the different pixels from image2
    diff_pixels = np.zeros_like(image2)
    diff_pixels[thresh != 0] = image2[thresh != 0]
    
    return diff_pixels

def main():
    # Create test images
    image1, image2 = create_test_images()
    
    # Find differences
    diff_pixels = find_differences(image1, image2)
    
    # Display the images and the different pixels image
    cv2.imshow('Image 1', image1)
    cv2.imshow('Image 2', image2)
    cv2.imshow('Different Pixels', diff_pixels)
    cv2.waitKey(0)  # Wait for any key press to close the window
    cv2.destroyAllWindows()
    
    # Optionally save the images and different pixels image
    cv2.imwrite('image1.jpg', image1)
    cv2.imwrite('image2.jpg', image2)
    cv2.imwrite('different_pixels.jpg', diff_pixels)

if __name__ == "__main__":
    main()
