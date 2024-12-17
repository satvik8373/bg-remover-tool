from rembg import remove
from PIL import Image
import io
import os

# Path to input and output directories
input_dir = './assets/'
output_dir = './output/'

# Function to remove the background
def remove_bg(input_image_path, output_image_path):
    with open(input_image_path, 'rb') as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)

    # Save the output image
    with open(output_image_path, 'wb') as output_file:
        output_file.write(output_data)

# Function to process all images in the 'assets' folder
def process_images():
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, filename)
            remove_bg(input_image_path, output_image_path)
            print(f"Processed: {filename}")

# Run the process
if __name__ == "__main__":
    process_images()
