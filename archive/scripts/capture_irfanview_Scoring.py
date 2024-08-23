import keyboard
import csv
import os
import time
import pygetwindow as gw

# Path to the folder containing the images
image_folder = 'path_to_your_images'

# Path to the CSV file where scores will be saved
score_file = 'image_scores.csv'

# Initialize a dictionary to store scores
scores = {}

# Function to load existing scores from a CSV file
def load_scores():
    if os.path.exists(score_file):
        with open(score_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header
            for row in csvreader:
                if len(row) == 2:  # Ensure correct format
                    image_name, score = row
                    scores[image_name] = score
        print(f"Loaded {len(scores)} existing scores from {score_file}")

# Function to write the scores to a CSV file
def write_scores():
    with open(score_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['image_name', 'score'])
        for image_name, score in scores.items():
            csvwriter.writerow([image_name, score])

# Function to capture the current image name from XnView
def get_current_image_name():
    # Get the active window title (XnView shows the filename in the window title)
    window = gw.getActiveWindow()
    if window and 'XnView' in window.title:
        # Extract the filename from the window title
        filename = window.title.split(' - ')[0]
        return os.path.basename(filename)
    return None

# Function to handle key press events
def on_key_press(e):
    if e.name in [str(i) for i in range(1, 10)]:
        score = e.name
        image_name = get_current_image_name()
        if image_name:
            scores[image_name] = score
            print(f"Recorded score {score} for {image_name}")
            write_scores()

# Load existing scores if the file exists
load_scores()

# Listen for key presses (1-9)
keyboard.on_press(on_key_press)

# Keep the script running
print("Listening for key presses (1-9) to score images...")

try:
    while True:
        time.sleep(1)
        if keyboard.is_pressed('esc'):
            print("Escape key pressed. Exiting...")
            break
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")

# Save scores upon exiting
write_scores()
print("All done. Goodbye!")