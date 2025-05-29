import pytesseract
import cv2
import numpy as np
from PIL import Image
import re

class OCREngine:
    def __init__(self):
        # Configure tesseract path for Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
    def preprocess_image(self, image_path):
        """Enhanced image preprocessing for better OCR accuracy"""
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply threshold to get image with only black and white
        _, threshold = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Deskew image (correct rotation)
        coords = np.column_stack(np.where(threshold > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        if abs(angle) > 0.5:  # Only rotate if angle is significant
            (h, w) = threshold.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            threshold = cv2.warpAffine(threshold, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return threshold
    
    def extract_text(self, image_path, lang='ben+eng'):
        """Extract text from image using Tesseract"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Convert back to PIL Image for pytesseract
            pil_img = Image.fromarray(processed_img)
            
            # Configure Tesseract
            custom_config = r'--oem 3 --psm 6'
            
            # Extract text
            text = pytesseract.image_to_string(pil_img, lang=lang, config=custom_config)
            
            return self.clean_text(text)
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return ""
    
    def clean_text(self, text):
        """Clean OCR output"""
        # Remove extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Replace multiple newlines
        text = re.sub(r' +', ' ', text)  # Replace multiple spaces
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')  # Common misrecognition
        text = text.replace('0', 'O')  # In contexts where it makes sense
        
        return text.strip()