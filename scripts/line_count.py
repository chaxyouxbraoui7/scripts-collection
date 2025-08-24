# A script that counts how many code lines there are in a file

import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(message)s')

line_count = tk.Tk()
line_count.lift() # makes the dialog appear on top
line_count.withdraw() # hide main window

project_directory = filedialog.askdirectory(title="Select the project directory")

if not project_directory:
    messagebox.showerror("Error", "No directory selected.")
    sys.exit(1)

if not os.path.isdir(project_directory):  
    logging.error("Invalid path.")
    messagebox.showerror("Error", "Invalid directory path.")
    sys.exit(1)

extensions = (".py")

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

def count_lines_in_project(project_folder):
    
    total_lines = 0
    non_empty_lines = 0
    file_count = 0

    print("\n\n-------------------------------------------------------------------------------------------------------------\n\n")
    
    for folder, _, files in os.walk(project_folder):
        
        for file in files:
            
            if file.endswith(extensions):
                file_path = os.path.join(folder, file)
                lines, non_empty = count_lines_in_file(file_path)
                file_count += 1
                
                logging.info(f"{file_count} - {file} - {lines} total lines | {non_empty} non-empty lines\n")

                total_lines += lines
                non_empty_lines += non_empty
    
    return total_lines, non_empty_lines

total_lines, non_empty_lines = count_lines_in_project(project_directory)

messagebox.showinfo("Line Count Summary", f"Total lines (including empty ones): {total_lines}\n\nTotal lines (excluding empty ones): {non_empty_lines}")