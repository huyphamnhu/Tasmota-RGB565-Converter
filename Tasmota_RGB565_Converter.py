# Prerequisites : python3, pip3, Pillow, numpy
# Usage : python3 Tasmota_RGB565_Converter.py [-h] [--size W*H] input_image_path
# Output file .rgb will be saved to current working directory

import argparse
from PIL import Image
import numpy as np
import os

# Function to convert an image to Tasmota RGB565 format
def func_converter(input_image_path, output_file_path, output_width, output_height):
    # Open the image
    image = Image.open(input_image_path)
    
    # Resize the image
    image = image.resize((output_width, output_height))
    
    # Convert the image to RGB
    image = image.convert("RGB")
    
    # Convert the image to a numpy array
    img_array = np.array(image)
    
    # Normalize and scale to RGB565
    red   = (img_array[:, :, 0] >> 3).astype(np.uint16)  # 5 bits for red (0-31)
    green = (img_array[:, :, 1] >> 2).astype(np.uint16)  # 6 bits for green (0-63)
    blue  = (img_array[:, :, 2] >> 3).astype(np.uint16)  # 5 bits for blue (0-31)
    
    # Combine the channels into one RGB565 format (16-bit)
    rgb565 = (red << 11) | (green << 5) | blue
    
    # Ensure the resulting array has the correct data type (uint16)
    rgb565 = rgb565.astype(np.uint16)
    
    # Open the output file and write the width and height as uint16 values (2 bytes each)
    with open(output_file_path, 'wb') as f:
        # Write width value (2 bytes as uint16)
        f.write(np.array([output_width], dtype=np.uint16).tobytes())
        
        # Write height value (2 bytes as uint16)
        f.write(np.array([output_height], dtype=np.uint16).tobytes())
        
        # Write the 16-bit RGB565 raw
        f.write(rgb565.tobytes())
    
    print(f"RGB565 image data saved as {output_file_path} (size: {output_width}x{output_height})")

# Main function to parse arguments and run the conversion
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert an image to RGB565 format.")
    parser.add_argument("input_image_path", type=str, help="Path to the input image (e.g., example.jpg)")
    
    # Add argument for output size in "width*height" format
    parser.add_argument("--size", type=str, help="Output size in 'width*height' format (e.g., 320*240)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no size argument is provided, use the original image size
    if args.size:
        # Split the size string at the '*' character and convert to integers
        try:
            output_width, output_height = map(int, args.size.split('*'))
        except ValueError:
            print("Error: Invalid size format. Use 'width*height', e.g., 320*240")
            return
    else:
        # If no size is provided, use the original image size
        with Image.open(args.input_image_path) as img:
            output_width, output_height = img.size
    
    # Extract the base name of the input file
    base_name = os.path.splitext(os.path.basename(args.input_image_path))[0]
    
    # Create the output file with the same name & .rgb extension
    output_file_path = f"{base_name}.rgb"
    
    # Call the conversion function with the parsed arguments
    func_converter(args.input_image_path, output_file_path, output_width, output_height)

if __name__ == "__main__":
    main()
