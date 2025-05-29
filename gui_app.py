import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from ocr_engine import OCREngine
from markdown_converter import MarkdownConverter
from file_handler import FileHandler

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bengali OCR to Markdown Converter")
        self.root.geometry("800x600")
        
        # Initialize components
        self.ocr_engine = OCREngine()
        self.markdown_converter = MarkdownConverter()
        self.file_handler = FileHandler()
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        ttk.Label(main_frame, text="Select Image or Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=60).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="Browse File", command=self.browse_file).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=2)
        
        # Obsidian vault path
        ttk.Label(main_frame, text="Obsidian Vault Path (optional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        vault_frame = ttk.Frame(main_frame)
        vault_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.vault_path_var = tk.StringVar()
        ttk.Entry(vault_frame, textvariable=self.vault_path_var, width=60).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(vault_frame, text="Browse", command=self.browse_vault).grid(row=0, column=1)
        
        # Language selection
        ttk.Label(main_frame, text="Language:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value="ben+eng")
        lang_combo = ttk.Combobox(main_frame, textvariable=self.lang_var, values=["ben+eng", "ben", "eng"])
        lang_combo.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Process", command=self.start_processing)
        self.process_btn.grid(row=6, column=0, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.output_text.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            self.file_path_var.set(folder)
    
    def browse_vault(self):
        folder = filedialog.askdirectory(title="Select Obsidian Vault Folder")
        if folder:
            self.vault_path_var.set(folder)
    
    def start_processing(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file or folder")
            return
        
        # Update file handler with vault path
        if self.vault_path_var.get():
            self.file_handler = FileHandler(self.vault_path_var.get())
        
        # Start processing in separate thread
        self.process_btn.config(state='disabled')
        self.progress.start()
        self.output_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def process_files(self):
        try:
            file_path = self.file_path_var.get()
            lang = self.lang_var.get()
            
            if os.path.isfile(file_path):
                # Single file processing
                self.log_output(f"Processing file: {file_path}")
                text = self.ocr_engine.extract_text(file_path, lang)
                
                if text.strip():
                    title = self.markdown_converter.extract_title_from_text(text)
                    markdown = self.markdown_converter.text_to_markdown(text, title)
                    saved_path = self.file_handler.save_markdown(markdown, title)
                    
                    self.log_output(f"Text extracted and saved to: {saved_path}")
                    self.log_output("\nExtracted text preview:")
                    self.log_output(text[:500] + "..." if len(text) > 500 else text)
                else:
                    self.log_output("No text could be extracted from the image")
                    
            elif os.path.isdir(file_path):
                # Batch processing
                self.log_output(f"Processing folder: {file_path}")
                processed_files = self.file_handler.batch_process_images(
                    file_path, self.ocr_engine, self.markdown_converter
                )
                self.log_output(f"Processed {len(processed_files)} files successfully")
                for file in processed_files:
                    self.log_output(f"- {file}")
            
        except Exception as e:
            self.log_output(f"Error: {str(e)}")
        
        finally:
            self.root.after(0, self.processing_complete)
    
    def log_output(self, message):
        self.root.after(0, lambda: self.output_text.insert(tk.END, message + "\n"))
        self.root.after(0, lambda: self.output_text.see(tk.END))
    
    def processing_complete(self):
        self.progress.stop()
        self.process_btn.config(state='normal')

def main():
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()