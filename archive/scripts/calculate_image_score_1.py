import os
import cv2
import numpy as np
from skimage import exposure
from PIL import Image
import torch
import piq
from torchvision import transforms
import torchvision.transforms as transforms


import warnings
warnings.filterwarnings("ignore", message="The parameter 'pretrained' is deprecated since 0.13")
warnings.filterwarnings("ignore", message="Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13")



import imquality.brisque as brisque
#import PIL.Image





def resize_image(image, max_dimension=2000):
    
    height, width = image.shape[:2]
    if max(height, width) > max_dimension:
        scale = max_dimension / float(max(height, width))
        new_size = (int(width * scale), int(height * scale))
        return cv2.resize(image, new_size)
    return image



def evaluate_images_in_folder(folder_path):
    results = []
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return results
    
    #print how many files it will process
    all_files = os.listdir(folder_path)
    valid_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Processing {len(valid_files)} image files in folder {folder_path}...\n")

    #Process each file
    file_count = 0
    for filename in all_files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Normalize to lowercase
            
            print(f"Processing file: {filename}...", end="")
            
            file_count += 1
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Failed to load image. Aborting.")
                continue
                
            print(f".", end=" ")
            
            resizedImage = resize_image(image,2000)
            score = brisque.score(resizedImage)
            roundedScore = round(score)
            #print("score: ", score)
            
            # results.append({
                # 'filename': filename,
                # 'score': score
            # })
            print(f"Score: {roundedScore}")

    print(f"\nFinished processing {file_count} files.\n")
    return results
    
    
if __name__ == "__main__":
    folder_path = "images"  # Replace with your actual folder path
    evaluate_images_in_folder(folder_path)
    
    # for result in results:
        # print(f"File: {result['filename']}")
        # print(f"  Score: {result['score']}\n")
    



# def crop_to_match(reference_image, target_size):
    # tgt_height, tgt_width = target_size
    # ref_height, ref_width = reference_image.shape[:2]
    
    # print(f"Cropping HQ reference image to {target_size}")

    # # Ensure that the reference image is large enough to be cropped
    # if ref_height < tgt_height or ref_width < tgt_width:
        # raise ValueError(f"Reference image size ({ref_height}x{ref_width}) is smaller than target size ({tgt_height}x{tgt_width}).")

    # # Calculate the starting points to crop from the center
    # start_y = (ref_height - tgt_height) // 2
    # start_x = (ref_width - tgt_width) // 2
    
    # # Perform the crop
    # cropped_image = reference_image[start_y:start_y + tgt_height, start_x:start_x + tgt_width]
    # return cropped_image

# def compute_sharpness(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    # return laplacian_var
    
# def compute_exposure(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    # hist_norm = hist.ravel()/hist.sum()
    # return hist_norm
    
# def calculate_piq_score(image):
    # print("Starting PIQ Score Calculation...")
    # reference_image = cv2.imread("reference_image.jpg")
    # target_size = image.shape[:2]
    
    # cropped_reference_image = crop_to_match(reference_image, target_size)
    # cropped_reference_tensor = transforms.ToTensor()(cropped_reference_image).unsqueeze(0)
            
    # lpips_loss = piq.LPIPS(reduction='none')
    # score = lpips_loss(image, cropped_reference_tensor)  # Compare with itself
    # return score.item()

# def evaluate_images_in_folder(folder_path):
    # results = []
    # print(f"Processing folder: {folder_path}")
    
    # if not os.path.exists(folder_path):
        # print(f"Folder not found: {folder_path}")
        # return results

    # # List all files in the folder
    # all_files = os.listdir(folder_path)
    # print(f"Files in folder: {all_files}")
    
    # file_count = 0
    # for filename in all_files:
        # if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Normalize to lowercase
            # file_count += 1
            # image_path = os.path.join(folder_path, filename)
            # print(f"Processing file: {filename}...")
            
            # image = cv2.imread(image_path)
            # if image is None:
                # print(f"Failed to load image: {filename}")
                # continue

            # # Resize the image before processing
            # print(f"Resizing file...")
            # image = resize_image(image, max_dimension=512)

            # print(f"Checking Sharpness...")
            # sharpness = compute_sharpness(image)
            
            # print(f"Checking exposure...")
            # exposure_hist = compute_exposure(image)
            
            # print(f"Calculating PIQ Score...")
            


            # # Convert the resized image to a tensor
            # transform = transforms.ToTensor()
            # image_tensor = transform(image).unsqueeze(0)
            # piq_score = calculate_piq_score(image_tensor)

            # underexposed = np.mean(exposure_hist[:50]) > 0.5
            # overexposed = np.mean(exposure_hist[-50:]) > 0.5

            # results.append({
                # 'filename': filename,
                # 'sharpness': sharpness,
                # 'underexposed': underexposed,
                # 'overexposed': overexposed,
                # 'piq_score': piq_score
            # })
            # print(f"Finished processing file: {filename}")
    
    # print(f"Processed {file_count} files.")
    # print("Finished processing all images.")
    # return results



# if __name__ == "__main__":
    # folder_path = "images"  # Replace with your actual folder path
    # results = evaluate_images_in_folder(folder_path)

    # for result in results:
        # print(f"File: {result['filename']}")
        # print(f"  Sharpness: {result['sharpness']}")
        # print(f"  Underexposed: {result['underexposed']}")
        # print(f"  Overexposed: {result['overexposed']}")
        # print(f"  Perceptual Quality (PIQ): {result['piq_score']}\n")
