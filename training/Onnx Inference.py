import argparse
import onnxruntime as ort
import numpy as np
import cv2

def preprocess_image(image_path):
    """
    Preprocess the image to match the model's input requirements
    1. Convert to grayscale
    2. Resize to (96, 96)
    3. Normalize to [0, 1]
    4. Add channel and batch dimensions
    """
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize the image to (96, 96)
    resized = cv2.resize(gray, (96, 96))
    # Normalize the image to [0, 1]
    normalized = resized.astype('float32') / 255.0
    # Add channel dimension (1, 96, 96)
    image_data = np.expand_dims(normalized, axis=0)
    # Add batch dimension (1, 1, 96, 96)
    image_data = np.expand_dims(image_data, axis=0)
    return image_data

def softmax(x):
    """
    Compute the softmax of a list of numbers x.
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def run_inference(model_path, image_path):
    # Load the ONNX model
    session = ort.InferenceSession(model_path)
    # Get input and output names from the model
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    # Preprocess the image
    image_data = preprocess_image(image_path)
    
    # Run the model inference
    result = session.run([output_name], {input_name: image_data})
    confidences = result[0][0]
    
    # Apply softmax to convert raw scores to probabilities
    probabilities = softmax(confidences)
    
    # Define gesture names based on the model's output classes
    gesture_names = ['palm', 'l', 'fist', 'thumb', 'index', 'ok', 'c', 'down']
    gesture_map = {0: 1, 1: 2, 2: 3, 3: 5, 4: 6, 5: 7, 6: 9, 7: 10}
    
    # Create a list of tuples with index, gesture name, and confidence
    results_with_confidences = [(gesture_map[i], gesture_names[i], probabilities[i]) for i in range(len(gesture_names))]
    
    # Sort results by confidence in descending order
    sorted_results = sorted(results_with_confidences, key=lambda x: x[2], reverse=True)
    
    # Print the results
    print("Recognition Results:")
    for idx, name, confidence in sorted_results:
        print(f"Gesture {idx} (Mapped): {name}, Confidence: {confidence:.4f}")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Run ONNX model inference on an image')
    parser.add_argument('model', type=str, help='Path to the ONNX model file')
    parser.add_argument('image', type=str, help='Path to the input image file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run inference
    run_inference(args.model, args.image)

if __name__ == '__main__':
    main()
