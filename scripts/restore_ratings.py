import argparse
import os
import csv
import subprocess
import keyboard
import shutil
from send2trash import send2trash
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored terminal output
init()

# ===============================
#  XMP Rating Update Script
#  -------------------------------
#  Author: Ryan Reed ryanreed87@gmail.com
#  Description:
#  This script reads image ratings
#  from a CSV file and updates the
#  corresponding XMP metadata in the
#  specified image files. The user
#  can also delete backup files after
#  the update process completes.
#
#  Features:
#  - Color-coded terminal output
#  - CSV error handling
#  - User-friendly prompts
#  - Support for multiple image formats
#  - Safe interruption with Escape key
# ===============================

# Set up argument parsing
parser = argparse.ArgumentParser(description="Restore image ratings from a CSV file by modifying XMP metadata.")
parser.add_argument('-imagefolder', required=True, help='Path (relative or absolute) to the folder containing images ie. path/to/image/folder')
parser.add_argument('-csvfile', required=True, help='Path (relative or absolute) to the CSV file with ratings ie. path/to/file.csv')

# Optional arguments for CSV header names
parser.add_argument('-csvheader_filename', default='Filename', help='Column header name for the filenames in the CSV file')
parser.add_argument('-csvheader_rating', default='Rating Nb', help='Column header name for the ratings in the CSV file')

# Parse the command-line arguments
args = parser.parse_args()

# Assign parsed arguments to variables
folder_path = args.imagefolder
csv_file = args.csvfile
csvheader_filename = args.csvheader_filename
csvheader_rating = args.csvheader_rating

# Define possible image file extensions
possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

# Initialize counters and terminal width
total_entries = 0
updated_files = 0
current_file = 0
terminal_width = shutil.get_terminal_size().columns

# Flag to control loop
continue_processing = True

# Reset style
RESET = Style.RESET_ALL

# Function to handle the Escape key press to stop the loop
def on_escape_press(event):
    global continue_processing
    continue_processing = False

# Hook the Escape key to stop processing
keyboard.on_press_key("esc", on_escape_press)

# Function to count the total entries in the CSV file
def count_csv_entries(csv_file):
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            total_entries = sum(1 for row in reader)
        return total_entries
    except FileNotFoundError:
        return f"\n\tError: The file {csv_file} was not found.\n"
    except PermissionError:
        return f"\n\tError: You do not have permission to access {csv_file}.\n"
    except csv.Error as e:
        return f"\n\tError reading CSV file: {e}\n"
    except Exception as e:
        return f"\n\tAn unexpected error occurred: {e}\n"

# Display welcome message centered in the terminal
welcome_text = "Welcome to the XMP Rating Update Script"
centered_text = welcome_text.center(terminal_width)
print(f"\n" + Fore.BLACK + Back.WHITE + " " * terminal_width)
print(centered_text)
print(" " * terminal_width + Style.RESET_ALL)

# Display image folder and CSV file paths
print(f"\n\tImage Folder Path:\t{Fore.GREEN + folder_path + RESET}")
print(f"\tReading CSV File:\t{Fore.GREEN + csv_file + RESET}...")

# Count total entries in the CSV file
total_entries = count_csv_entries(csv_file)
if isinstance(total_entries, int):
    print(f"\tEntries found:\t\t{Fore.CYAN}{total_entries}{RESET}\n")
    request_continue = input(f"\tDo you want to update the ratings of {Fore.CYAN}{total_entries}{RESET} image files? (y/n): ").strip().lower()
else:
    print(Fore.RED + total_entries + RESET)
    request_continue = 'n'

# Proceed with updating ratings if the user agrees
if request_continue == 'y':
    # Read the CSV file and process each entry
    with open(csv_file, mode='r') as file:
        print(f"\n\n\tAttempting to update the XMP ratings of {Fore.CYAN}{total_entries}{RESET} files. {Fore.YELLOW}Press Escape key at any time to abort early.{RESET}\n")
        
        # Iterate through each row in the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            # Check for early exit
            if not continue_processing:
                print(f"\t\t{Fore.YELLOW}Stopping...{RESET}")
                break
            
            # Increment file counter and extract filename and rating
            current_file += 1
            filename = row[csvheader_filename]
            rating = row[csvheader_rating].strip()
            
            # Clear the previous line and print the current processing status
            print(f"\r{' ' * terminal_width}", end="\r")
            print(f"\t\t{current_file} of {total_entries}\tFile:  {Fore.CYAN + filename + RESET} \tRating: {Fore.CYAN}{rating}{RESET} \tStatus: {Fore.CYAN}Finding File...{RESET}", end="\r")
            
            # Try to find the file with one of the possible extensions
            file_found = False
            for ext in possible_extensions:
                file_path = os.path.join(folder_path, filename + ext)
                
                # If the file is found, attempt to update the XMP rating
                if os.path.isfile(file_path):
                    print(f"\r{' ' * terminal_width}", end="\r")
                    print(f"\t\t{current_file} of {total_entries}\tFile:  {Fore.CYAN + filename + ext + RESET} \tRating: {Fore.CYAN}{rating}{RESET} \tStatus: {Fore.CYAN}Update in progress...{RESET}", end="\r")
                    
                    # Run ExifTool to update the rating
                    result = subprocess.run([
                        'exiftool',
                        '-m',  # Suppress minor warnings
                        f'-XMP:Rating={rating}',
                        file_path
                    ], capture_output=True, text=True)
                    
                    # Check the result of the ExifTool command
                    if result.returncode == 0:
                        print(f"\r{' ' * terminal_width}", end="\r")
                        print(f"\t\t{current_file} of {total_entries}\tFile:  {Fore.CYAN + filename + ext + RESET} \tRating: {Fore.CYAN}{rating}{RESET} \tStatus: {Fore.GREEN}Updated ✔{RESET}")
                        updated_files += 1
                    else:
                        print(f"\r{' ' * terminal_width}", end="\r")
                        print(f"\t\t{Fore.RED}{current_file} of {total_entries}\tFile:  {filename}{ext} \tRating: {rating} \tStatus: ✘ {result.stderr.strip()}{RESET}")
                    
                    file_found = True
                    break
            
            # If the file was not found, display an error message
            if not file_found:
                print(f"\r{' ' * terminal_width}", end="\r")
                print(f"\t\t{current_file} of {total_entries}\tFile:  {Fore.CYAN}{filename}{RESET} \tRating: {Fore.CYAN}{rating}{RESET} \tStatus: {Fore.RED}✘  [File not found]{RESET}")
    
    # Print summary of the process
    print(f"\n\t\t{Fore.CYAN}{current_file}{RESET} of {Fore.CYAN}{total_entries}{RESET} File Ratings Processed")
    print(f"\t\t{Fore.GREEN}{updated_files} File Ratings Updated{RESET}")
    print(f"\t\t{Fore.RED}{current_file - updated_files} File Ratings Failed{RESET}\n")

    # Ask the user if they want to delete the backups
    delete_backups = input(f"\tDo you want to send {Fore.CYAN}{updated_files}{RESET} backup files to recycle bin? (y/n): ").strip().lower()

    if delete_backups == 'y':
        print(f"\n\t\tMoving {Fore.CYAN}{updated_files}{RESET} backup files to recycle bin...")
        delete_counter = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('_original'):
                    delete_counter += 1
                    backup_file_path = os.path.join(root, file)
                    
                    print(f"\r{' ' * terminal_width}", end="\r")
                    print(f"\t\tDeleting {Fore.CYAN}{delete_counter}{RESET} of {Fore.CYAN}{updated_files}{RESET} \tFile: {Fore.CYAN + file + RESET}", end="\r")
                    
                    send2trash(backup_file_path)
        print(f"\r{' ' * terminal_width}", end="\r")
        print(f"\t\t{Fore.GREEN}{delete_counter} of {updated_files} backup files sent to recycle bin.{RESET}")

    else:
        print(f"\t\t{Fore.YELLOW}No backups deleted.{RESET}")

    print(f"\n\n\t{Fore.GREEN}Task Complete. Exiting.{RESET}\n\n")

else:
    print(f"\n\t{Fore.YELLOW}Exiting. No files modified.{RESET}\n\n")
