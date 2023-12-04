# KA enhancement
import os
import cv2
import subprocess
import glob
import shutil
import numpy as np
import argparse
from natsort import natsorted

def find_images(root_dir, camera):
    pattern = os.path.join(root_dir, '**', 'Image', camera, '*.png')
    return natsorted([os.path.normpath(p) for p in glob.glob(pattern, recursive=True)])

def create_sbs_video(input_directory):
    output_video = os.path.join(input_directory, os.path.basename(input_directory) + ".mp4")
    left_images = find_images(input_directory, 'camera_0')
    right_images = find_images(input_directory, 'camera_1')
    
    temp_dir = os.path.join(input_directory, "temp_images")
    os.makedirs(temp_dir, exist_ok=True)
    print(temp_dir)
    
    for idx, (left_img_path, right_img_path) in enumerate(zip(left_images, right_images)):
        left_img = cv2.imread(left_img_path)
        right_img = cv2.imread(right_img_path)

        # Create side-by-side image
        sbs_image = np.concatenate((left_img, right_img), axis=1)
        temp_img_path = os.path.join(temp_dir, f"{idx+1}.png")  # Naming images as 1.png, 2.png, etc.
        cv2.imwrite(temp_img_path, sbs_image)

    # Use FFmpeg to create the video from the SBS images
    ffmpeg_cmd = ['ffmpeg', '-framerate', '30', '-i', os.path.join(temp_dir, '%d.png'), 
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_video]
    subprocess.run(ffmpeg_cmd)


    # Clean up temporary images
    #shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a SBS stereo video from images.")
    parser.add_argument("input_directory", help="Path to the input directory containing the images.")
    args = parser.parse_args()

    create_sbs_video(args.input_directory)
