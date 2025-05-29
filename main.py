#!/usr/bin/env python3
"""
Bengali OCR to Markdown Converter
Main entry point for the application
"""

import sys
import argparse
from gui_app import main as gui_main
from full_test import run_complete_test

def main():
    parser = argparse.ArgumentParser(description='Bengali OCR to Markdown Converter')
    parser.add_argument('--test', action='store_true', help='Run complete test')
    parser.add_argument('--gui', action='store_true', help='Launch GUI (default)')
    
    args = parser.parse_args()
    
    if args.test:
        run_complete_test()
    else:
        # Default to GUI
        gui_main()

if __name__ == "__main__":
    main()