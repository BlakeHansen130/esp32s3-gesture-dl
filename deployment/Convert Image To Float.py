import cv2
import numpy as np
import argparse
import os

def process_image(image_path):
    """
    Process image following the same steps as your quantization workflow:
    1. Read image
    2. Convert to grayscale
    3. Resize to 96x96
    4. Normalize to [0, 1] as float
    """
    # Read and preprocess image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize to 96x96
    resized = cv2.resize(gray, (96, 96))
    
    # Normalize to [0,1] as float
    normalized = resized.astype('float32') / 255.0
    
    return normalized

def generate_header(data, output_path):
    """Generate C++ header file with the image data."""
    with open(output_path, 'w') as f:
        f.write("#pragma once\n\n")
        f.write("// Auto-generated header file for preprocessed image data\n")
        f.write("// Image size: 96x96 pixels, normalized to float\n\n")
        
        f.write("const float test_image_data[9216] = {\n    ")
        
        # Convert data to string representation
        data_str = [f"{x:.6f}" for x in data.flatten()]
        
        # Write data in chunks of 8 numbers per line
        chunk_size = 8
        for i in range(0, len(data_str), chunk_size):
            chunk = data_str[i:i + chunk_size]
            f.write(", ".join(chunk))
            if i + chunk_size < len(data_str):
                f.write(",\n    ")
            else:
                f.write("\n")
        
        f.write("};\n")

def main():
    parser = argparse.ArgumentParser(description='Convert image to C++ header file')
    parser.add_argument('image_path', help='Path to the input image')
    args = parser.parse_args()

    try:
        # Process image
        data = process_image(args.image_path)
        
        # Ensure model directory exists
        os.makedirs('model', exist_ok=True)
        
        # Generate header file
        output_path = os.path.join('model', 'test_image.hpp')
        generate_header(data, output_path)
        
        print(f"Successfully generated header file: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
