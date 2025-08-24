# A script that generates the provided directory structure as a tree

import os
from tkinter import filedialog, Tk

def gen_dir_str(start_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs_, files in os.walk(start_path): # walk through all the folders, dirs, files and return them
            level = root.replace(start_path, '').count(os.sep) # depth of the current folder relativ to the start & the os.sep is the system path separator
            pref = '│   ' * (level - 1) + '├── ' if level > 0 else '' # tree style prefix for the folders
            f.write(f"{pref}{os.path.basename(root)}/\n") # writting the folder name, os.path.basname(root) gives the name only
            
            conntent = '│   ' * level + '├── ' # content handlaning
            for i, file in enumerate(sorted(files)):
                if i == len(files) - 1:
                    conntent = '│   ' * level + '└── ' # last item
                f.write(f"{conntent}{file}\n")

def main():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder to Generate the Directory Structure")
    if not folder_path:
        print("No folder selected")
        return
    
    output_path = os.path.join(folder_path, "dir_structure.txt")
    gen_dir_str(folder_path, output_path)
    
    print(f"Folder structure saved to: {output_path}")
    
    # open the result automatically
    try:
        if os.name == 'nt':  # for Windows
            os.startfile(output_path)
        elif hasattr(os, 'uname') and os.uname().sysname == 'Darwin':  # for Mac
            os.system(f'open "{output_path}"')
        else:  # for Linux
            if os.system(f'xdg-open "{output_path}"') != 0:
                print("Could not open the file automatically! Please open it manually.")
                
    except Exception as e:
        print(f"Error opening the file: {e}")

if __name__ == "__main__":
    main()