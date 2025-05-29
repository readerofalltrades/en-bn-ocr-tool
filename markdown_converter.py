import re
from datetime import datetime

class MarkdownConverter:
    def __init__(self):
        self.patterns = {
            'header1': r'^([A-Z][^।\n]*?)[\s]*$',
            'header2': r'^([০-৯][\)\.]\s*[^।\n]*?)[\s]*$',
            'bullet': r'^[\-\*\•]\s*(.+)$',
            'numbered': r'^([০-৯]+[\.\)]\s*.+)$',
            'emphasis': r'\*([^*]+)\*',
            'strong': r'\*\*([^*]+)\*\*'
        }
    
    def text_to_markdown(self, text, title=""):
        """Convert plain text to markdown format"""
        lines = text.split('\n')
        markdown_lines = []
        
        # Add frontmatter
        if title:
            markdown_lines.extend(self._create_frontmatter(title))
        
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    in_list = False
                markdown_lines.append('')
                continue
            
            # Process line based on patterns
            processed_line = self._process_line(line)
            
            # Check if it's a list item
            if processed_line.startswith(('- ', '* ', '1. ')):
                in_list = True
            elif in_list and not processed_line.startswith((' ', '\t')):
                in_list = False
            
            markdown_lines.append(processed_line)
        
        return '\n'.join(markdown_lines)
    
    def _create_frontmatter(self, title):
        """Create YAML frontmatter for Obsidian"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [
            "---",
            f"title: {title}",
            f"created: {timestamp}",
            "tags: [notes, ocr]",
            "---",
            ""
        ]
    
    def _process_line(self, line):
        """Process individual line for markdown conversion"""
        # Headers (Bengali/English mixed)
        if re.match(r'^[A-ZА-Я][^।\n]{10,}$', line):
            return f"## {line}"
        
        # Numbered lists (Bengali numerals)
        if re.match(r'^[০-৯]+[\.\)]\s*.+', line):
            return f"1. {line[2:].strip()}"
        
        # Bullet points
        if re.match(r'^[\-\*\•]\s*.+', line):
            return f"- {line[1:].strip()}"
        
        # Emphasis patterns
        line = re.sub(r'\*([^*]+)\*', r'*\1*', line)
        line = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', line)
        
        return line
    
    def extract_title_from_text(self, text):
        """Extract potential title from first few lines"""
        lines = text.split('\n')[:3]
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                # Clean title
                title = re.sub(r'[^\w\s\u0980-\u09FF]', '', line)
                return title[:50] if title else "Untitled Note"
        return "Untitled Note"