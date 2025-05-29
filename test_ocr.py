from ocr_engine import OCREngine
import os

def test_ocr():
    ocr = OCREngine()
    
    # Test with a sample image
    image_path = "sample_note.jpg"  # Place your test image here
    
    if os.path.exists(image_path):
        text = ocr.extract_text(image_path)
        print("Extracted Text:")
        print("-" * 50)
        print(text)
        print("-" * 50)
    else:
        print(f"Please place a test image at {image_path}")

if __name__ == "__main__":
    test_ocr()