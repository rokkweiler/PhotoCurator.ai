import os
import csv
import cv2

# Function to get the zoomed region centered around the mouse position
def get_zoomed_region(image, zoom_scale, center_x, center_y):
    h, w = image.shape[:2]
    
    # Calculate the size of the zoomed region
    new_w = int(w * 100 / zoom_scale)
    new_h = int(h * 100 / zoom_scale)
    
    # Ensure the zoomed area is within bounds
    x1 = max(0, min(center_x - new_w // 2, w - new_w))
    y1 = max(0, min(center_y - new_h // 2, h - new_h))
    
    # Calculate the bottom-right corner of the zoomed area
    x2 = x1 + new_w
    y2 = y1 + new_h
    
    # Crop and resize the ROI to fill the window while maintaining aspect ratio
    roi = image[y1:y2, x1:x2]
    return roi, (x1, y1, new_w, new_h)

# Function to maintain aspect ratio and fit image to window size
def fit_to_window(image, window_width, window_height):
    h, w = image.shape[:2]
    aspect_ratio = w / h
    
    if window_width / window_height > aspect_ratio:
        # Window is wider relative to its height, so fit height
        new_height = window_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Window is taller relative to its width, so fit width
        new_width = window_width
        new_height = int(new_width / aspect_ratio)
    
    # Resize image to fit within the window while maintaining aspect ratio
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    return resized_image

# Mouse callback function to update the zoom level and position
def mouse_callback(event, x, y, flags, param):
    global zoom_scale, mouse_x, mouse_y, img, x_offset, y_offset, zoomed_region
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_scale -= 5  # Zoom in faster
        else:
            zoom_scale += 5  # Zoom out faster
        zoom_scale = max(1, min(zoom_scale, 1000))  # Allow zoom scale between 1% and 1000%
        
        # Update zoomed region
        zoomed_region, _ = get_zoomed_region(img, zoom_scale, mouse_x + x_offset, mouse_y + y_offset)

    elif event == cv2.EVENT_MOUSEMOVE:
        # Calculate movement relative to the zoomed region
        x_offset = int((x - mouse_x) * (100 / zoom_scale))
        y_offset = int((y - mouse_y) * (100 / zoom_scale))
        mouse_x, mouse_y = x, y
        
        # Update zoomed region with new offsets
        zoomed_region, _ = get_zoomed_region(img, zoom_scale, mouse_x + x_offset, mouse_y + y_offset)

# Path to the folder containing the images
image_folder = 'images/yettoscore'

# Path to the CSV file where scores will be saved
score_file = 'images/image_scores.csv'

# Number of images after which to write scores to the file
batch_size = 5

# Initialize variables
scores = []
image_names = sorted(os.listdir(image_folder))
initial_zoom_height = 1800  # Desired initial height in pixels
mouse_x, mouse_y = 0, 0  # Initialize mouse position
x_offset, y_offset = 0, 0  # Offsets for panning

if not image_names:
    print("No images found in the specified directory.")
    exit(1)

# Loop through the images
for i, image_name in enumerate(image_names):
    image_path = os.path.join(image_folder, image_name)
    
    # Load the image
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    # Set initial zoom scale based on desired initial height
    zoom_scale = int(h / (initial_zoom_height / 100))
    
    # Create a named window and set a mouse callback
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Image', mouse_callback)
    
    # Resize the window to match the image aspect ratio initially
    initial_display_img = fit_to_window(img, 800, 800)
    cv2.resizeWindow('Image', initial_display_img.shape[1], initial_display_img.shape[0])
    
    # Initial zoom region setup
    zoomed_region, _ = get_zoomed_region(img, zoom_scale, mouse_x, mouse_y)
    
    while True:
        # Fit the zoomed image to the current window size while maintaining aspect ratio
        display_img = fit_to_window(zoomed_region, initial_display_img.shape[1], initial_display_img.shape[0])
        
        # Display the zoomed image
        cv2.imshow('Image', display_img)
        
        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF
        
        # Break the loop if 'q' is pressed
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
    
    # Prompt for the score after closing the image
    score = input(f"Enter score for {image_name}: ")
    scores.append([image_name, score])
    
    # Write scores to file after every batch_size images
    if (i + 1) % batch_size == 0 or (i + 1) == len(image_names):
        with open(score_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if i == 0:  # Write header only once, at the first batch
                csvwriter.writerow(['image_name', 'score'])
            csvwriter.writerows(scores)
        scores.clear()

print("Scoring complete and all scores have been saved.")
