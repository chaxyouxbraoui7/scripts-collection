# A script that counts how many code lines there are in files.

# User can choose now between files extensions, directory or just a file

import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.simpledialog as simpledialog

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(message)s')

line_count = tk.Tk()
line_count.lift() # makes the dialog appear on top
line_count.withdraw() # hide main window

choice = messagebox.askquestion("Choose Input", "Yes = File | No = Directory")

if choice == 'yes':
    path = filedialog.askopenfilename(title="Select a file")
else:
    path = filedialog.askdirectory(title="Select a directory")

if not path:
    messagebox.showerror("Error", "No file or directory selected.")
    sys.exit(1)

def detect_extensions(folder):
    
    """Detect all unique file extensions in a folder."""
    
    exts = set()
    for root, _, files in os.walk(folder):
        for file in files:
            if '.' in file:
                exts.add(os.path.splitext(file)[1])
    return tuple(exts)

# Only detect extensions if path is a directory
if os.path.isdir(path):
    extensions_detected = detect_extensions(path)
    if extensions_detected:
        # Ask user if they want to include all detected extensions
        include_all = messagebox.askyesno(
            "Extensions Detected",
            f"Detected file extensions: {', '.join(extensions_detected)}\n\nCount all of them?"
        )
        if include_all:
            extensions = None  # Count all files
        else:
            # Let user choose a subset
            ext_input = simpledialog.askstring(
                "Select Extensions",
                "Enter extensions to include separated by commas (from detected):"
            )
            if ext_input:
                extensions = tuple(e.strip() for e in ext_input.split(","))
            else:
                extensions = None
    else:
        extensions = None  # no files found, count all
else:
    extensions = None  # single file, no filtering needed

def count_lines_in_file(path_):
    """Function to count the number of lines in a given file."""
    total_lines = 0
    non_empty_lines = 0
    try:
        
        with open(path_, "r", encoding="utf-8") as f:
            for line in f:
                total_lines += 1
                if line.strip():
                    non_empty_lines += 1
                    
    except Exception as e:
        logging.error(f"Error reading {path_}: {e}")
    return total_lines, non_empty_lines

def count_lines_in_project(project_folder, extensions=None):
    
    total_lines = 0
    non_empty_lines = 0
    file_count = 0

    print("\n\n-------------------------------------------------------------------------------------------------------------\n\n")
    
    for folder, _, files in os.walk(project_folder):
        
        for file in files:
            
            if extensions is None or file.endswith(extensions):
                file_path = os.path.join(folder, file)
                lines, non_empty = count_lines_in_file(file_path)
                file_count += 1
                
                logging.info(f"{file_count} - {file} - {lines} total lines | {non_empty} non-empty lines\n")

                total_lines += lines
                non_empty_lines += non_empty
    
    return total_lines, non_empty_lines

if os.path.isfile(path):
    total_lines, non_empty_lines = count_lines_in_file(path)
else:
    total_lines, non_empty_lines = count_lines_in_project(path, extensions)

messagebox.showinfo("Line Count Summary", f"Total lines (including empty ones): {total_lines}\n\nTotal lines (excluding empty ones): {non_empty_lines}")