import cv2
import numpy as np
import os

def parse_hpp_file(file_path):
    """Parse the HPP file and extract the array data."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the array data between curly braces
    start = content.find('{') + 1
    end = content.rfind('}')
    data_str = content[start:end]
    
    # Split and convert to integers
    values = [int(x.strip()) for x in data_str.split(',') if x.strip()]
    return np.array(values, dtype=np.int8)

def reconstruct_image(data):
    """Reconstruct image from int8 array."""
    # Reshape to 96x96
    img = data.reshape(96, 96)
    
    # Convert back from quantized values to [0,255]
    img = (img.astype(float) / 128 * 255).clip(0, 255).astype(np.uint8)
    return img

def main():
    try:
        # Read hpp file
        hpp_path = os.path.join('model', 'test_image.hpp')
        data = parse_hpp_file(hpp_path)
        
        # Reconstruct and save image
        img = reconstruct_image(data)
        output_path = 'reconstructed_image.png'
        cv2.imwrite(output_path, img)
        
        print(f"Successfully generated image: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()