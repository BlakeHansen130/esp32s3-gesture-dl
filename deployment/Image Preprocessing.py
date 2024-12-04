#!/usr/bin/env python3
import cv2
import numpy as np
import os
import sys
from pathlib import Path

def preprocess_image(image_path, output_path=None):
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"无法读取图片: {image_path}")
    
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    lower = np.array([0, 135, 85], dtype=np.uint8)
    upper = np.array([255, 180, 135], dtype=np.uint8)
    skin_mask = cv2.inRange(ycrcb, lower, upper)
    
    kernel = np.ones((5,5), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    
    # 将掩码值缩放到127以内
    skin_mask = (skin_mask / 2).astype(np.uint8)
    
    if output_path:
        cv2.imwrite(output_path, skin_mask)
    return skin_mask
    
if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("使用方法: python script.py <input_image>")
       sys.exit(1)
       
   input_path = sys.argv[1]
   output_dir = "../dataset/Web_Images_Processed_Versions"
   input_filename = os.path.basename(input_path)
   input_name, input_ext = os.path.splitext(input_filename)
   output_filename = f"{input_name}_processed{input_ext}"
   output_path = os.path.join(output_dir, output_filename)

   try:
       preprocess_image(input_path, output_path)
       print(f"处理完成: {output_path}")
   except Exception as e:
       print(f"处理失败: {e}")
       sys.exit(1)