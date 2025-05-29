import os
import sys
from ocr_engine import OCREngine
from markdown_converter import MarkdownConverter
from file_handler import FileHandler

def run_complete_test():
    print("=== Bengali OCR to Markdown - Complete Test ===\n")
    
    # Initialize components
    ocr = OCREngine()
    converter = MarkdownConverter()
    handler = FileHandler("./test_output")  # Create test output folder
    
    # Test with sample image (you need to provide this)
    test_image = "test_bengali_note.jpg"
    
    if not os.path.exists(test_image):
        print(f"Please place a test Bengali image at: {test_image}")
        print("You can take a photo of handwritten Bengali notes for testing")
        return
    
    print(f"1. Processing image: {test_image}")
    
    # Step 1: OCR
    print("   - Extracting text...")
    text = ocr.extract_text(test_image, lang='ben+eng')
    print(f"   - Extracted {len(text)} characters")
    
    if not text.strip():
        print("   - No text extracted. Check image quality and Bengali language pack installation.")
        return
    
    # Step 2: Convert to Markdown
    print("   - Converting to markdown...")
    title = converter.extract_title_from_text(text)
    markdown = converter.text_to_markdown(text, title)
    
    # Step 3: Save file
    print("   - Saving markdown file...")
    saved_path = handler.save_markdown(markdown, title)
    
    # Step 4: Display results
    print(f"\n2. Results:")
    print(f"   - Title: {title}")
    print(f"   - Saved to: {saved_path}")
    print(f"\n3. Text Preview:")
    print("=" * 50)
    print(text[:300] + "..." if len(text) > 300 else text)
    print("=" * 50)
    print(f"\n4. Markdown Preview:")
    print("=" * 50)
    print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
    print("=" * 50)
    
    print(f"\n✅ Test completed successfully!")
    print(f"Check the output file at: {saved_path}")

if __name__ == "__main__":
    run_complete_test()