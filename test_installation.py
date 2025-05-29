import pytesseract 
import cv2 #python module for OpenCV
from PIL import Image #Imports the Image class from Python Imaging Library 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print("Available languages:", pytesseract.get_languages())
print("Tesseract version:", pytesseract.get_tesseract_version())