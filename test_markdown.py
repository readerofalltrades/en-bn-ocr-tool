from markdown_converter import MarkdownConverter

def test_markdown_conversion():
    converter = MarkdownConverter()
    
    # Sample text (mix this with your OCR output)
    sample_text = """গণিত নোট
১. সূত্রসমূহ
- a² + b² = c²
- sin²θ + cos²θ = 1
২. উদাহরণ
পরীক্ষার জন্য গুরুত্वপূর্ণ"""
    
    title = converter.extract_title_from_text(sample_text)
    markdown = converter.text_to_markdown(sample_text, title)
    
    print("Original Text:")
    print(sample_text)
    print("\nMarkdown Output:")
    print(markdown)

if __name__ == "__main__":
    test_markdown_conversion()