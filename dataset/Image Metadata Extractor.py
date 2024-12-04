import sys
import os
import cv2
import numpy as np
from PIL import Image, ExifTags
from PIL import ImageCms

def get_image_metadata(image_path):
    # Load image using OpenCV and Pillow
    try:
        img_cv = cv2.imread(image_path)
        img_pil = Image.open(image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)

    # Basic Information
    width, height = img_pil.size
    mode = img_pil.mode
    format = img_pil.format
    print(f"Image Format: {format}")
    print(f"Image Mode (Color Type): {mode}")
    print(f"Resolution (Width x Height): {width} x {height}")

    # Bit Depth
    if img_pil.mode in ['1', 'L', 'P']:
        bit_depth = 8
    elif img_pil.mode == 'RGB':
        bit_depth = 24
    elif img_pil.mode == 'RGBA':
        bit_depth = 32
    elif img_pil.mode == 'I;16':
        bit_depth = 16
    else:
        bit_depth = len(img_pil.getbands()) * 8
    print(f"Bit Depth: {bit_depth} bits")

    # Color Space
    try:
        profile = img_pil.info.get("icc_profile")
        if profile:
            img_profile = ImageCms.getProfileName(profile)
            print(f"Color Profile: {img_profile}")
        else:
            print("Color Profile: Not found (may be sRGB)")
    except Exception as e:
        print(f"Color Profile: Error reading color profile ({e})")

    # Channels Information
    channels = len(img_pil.getbands())
    channel_descriptions = {
        'R': 'Red',
        'G': 'Green',
        'B': 'Blue',
        'A': 'Alpha (Transparency)',
        'L': 'Luminance (Grayscale)',
        'P': 'Palette-based'
    }
    channel_names = [channel_descriptions.get(band, band) for band in img_pil.getbands()]
    print(f"Number of Channels: {channels}")
    print(f"Channels: {', '.join(channel_names)}")

    # File Size
    file_size = os.path.getsize(image_path)
    print(f"File Size: {file_size / 1024:.2f} KB ({file_size / (1024 * 1024):.2f} MB)")

    # Compression
    compression = img_pil.info.get("compression", "Unknown")
    print(f"Compression Type: {compression}")

    # Metadata (EXIF)
    exif_data = img_pil._getexif() if hasattr(img_pil, '_getexif') else None
    if exif_data:
        print("EXIF Metadata:")
        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            print(f"  {tag_name}: {value}")
    else:
        print("EXIF Metadata: Not found")

    # DPI (Dots Per Inch)
    dpi = img_pil.info.get('dpi', (72, 72))
    print(f"DPI (Dots Per Inch): {dpi[0]} x {dpi[1]}")

    # Image Matrix
    if img_cv is not None:
        img_array = np.array(img_cv)
        print(f"Image Matrix Shape (Height x Width x Channels): {img_array.shape}")
        print(f"Image Data Type: {img_array.dtype}")

    # Color Histogram (for RGB images)
    if mode == 'RGB':
        print("Color Histogram (RGB):")
        for i, color in enumerate(['Blue', 'Green', 'Red']):
            histogram = cv2.calcHist([img_cv], [i], None, [256], [0, 256])
            print(f"  {color} Channel Histogram: {histogram.flatten()[:10]} (First 10 Bins)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print("Error: File does not exist.")
        sys.exit(1)

    get_image_metadata(image_path)
