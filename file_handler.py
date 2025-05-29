import os
import re
from pathlib import Path
from datetime import datetime

class FileHandler:
    def __init__(self, obsidian_vault_path=""):
        self.obsidian_vault_path = obsidian_vault_path
        self.output_folder = "OCR_Notes"
        self._ensure_output_folder()
    
    def _ensure_output_folder(self):
        """Create output folder if it doesn't exist"""
        if self.obsidian_vault_path:
            full_path = os.path.join(self.obsidian_vault_path, self.output_folder)
        else:
            full_path = self.output_folder
        
        Path(full_path).mkdir(parents=True, exist_ok=True)
        self.full_output_path = full_path
    
    def save_markdown(self, markdown_content, title=""):
        """Save markdown content to file"""
        if not title:
            title = "Note"
        
        # Clean filename
        filename = self._clean_filename(title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}.md"
        
        filepath = os.path.join(self.full_output_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return None
    
    def _clean_filename(self, title):
        """Clean title for use as filename"""
        # Remove special characters, keep Bengali and English
        cleaned = re.sub(r'[^\w\s\u0980-\u09FF-]', '', title)
        cleaned = re.sub(r'\s+', '_', cleaned.strip())
        return cleaned[:30] if cleaned else "note"
    
    def batch_process_images(self, image_folder, ocr_engine, markdown_converter):
        """Process all images in a folder"""
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        processed_files = []
        
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(supported_formats):
                image_path = os.path.join(image_folder, filename)
                print(f"Processing: {filename}")
                
                # Extract text
                text = ocr_engine.extract_text(image_path)
                
                if text.strip():
                    # Convert to markdown
                    title = markdown_converter.extract_title_from_text(text)
                    markdown = markdown_converter.text_to_markdown(text, title)
                    
                    # Save file
                    saved_path = self.save_markdown(markdown, title)
                    if saved_path:
                        processed_files.append(saved_path)
                else:
                    print(f"No text extracted from {filename}")
        
        return processed_files