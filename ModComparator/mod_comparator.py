import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

TITLE = "Mod Comparator"
GEOMETRY = '650x300'
RESIZABLE = False
EXTENSION = '.txt'

def save_settings(settings):
    
    try:
    
        with open("settings.json", "w") as file:
            json.dump(settings, file)
        
        print("Saved settings", settings)
    
    except IOError as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

def load_settings():
    
    try:
        
        with open("settings.json", "r") as file:
            return json.load(file)
            
    except FileNotFoundError:
        
        print("Settings file not found.")
        return {}

def create_widgets(Tk, settings):
    
    entries = {}
    
    # File A
    tk.Label(Tk, text="Input Text File A:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entries['fileA_entry'] = tk.Entry(Tk, width=50)
    entries['fileA_entry'].grid(row=0, column=1, padx=10, pady=5)
    tk.Button(Tk, text="Browse", command=lambda: browse_fileA(entries)).grid(row=0, column=2, padx=0, pady=5)
    
    # File B
    tk.Label(Tk, text="Input Text File B:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entries['fileB_entry'] = tk.Entry(Tk, width=50)
    entries['fileB_entry'].grid(row=1, column=1, padx=10, pady=5)
    tk.Button(Tk, text="Browse", command=lambda: browse_fileB(entries)).grid(row=1, column=2, padx=0, pady=5)
    
    # Output Directory
    tk.Label(Tk, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    entries['outputDir_entry'] = tk.Entry(Tk, width=50)
    entries['outputDir_entry'].grid(row=2, column=1, padx=10, pady=5)
    tk.Button(Tk, text="Browse", command=lambda: browse_outputDir(entries)).grid(row=2, column=2, padx=0, pady=5)
    
    # Output File Name
    tk.Label(Tk, text="Output File Name (without extension):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    entries['outputName_entry'] = tk.Entry(Tk, width=50)
    entries['outputName_entry'].grid(row=3, column=1, padx=10, pady=5)
    
    # Comparison Type
    entries['searchOption_entry'] = tk.StringVar()
    tk.Label(Tk, text="Comparison Type:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Radiobutton(Tk, text="Find Matches", variable=entries['searchOption_entry'], value="match").grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
    tk.Radiobutton(Tk, text="Find Differences", variable=entries['searchOption_entry'], value="differ").grid(row=4, column=1, padx=125, pady=5, sticky=tk.W)
    
    # Process Button
    tk.Button(Tk, text="Find Differences", command=lambda: process(entries)).grid(row=5, column=0, columnspan=3, pady=20)
    
    # Set default values
    entries['fileA_entry'].insert(0, settings.get('fileA', ''))
    entries['fileB_entry'].insert(0, settings.get('fileB', ''))
    entries['outputDir_entry'].insert(0, settings.get('outputDir', ''))
    entries['outputName_entry'].insert(0, settings.get('outputName', ''))
    entries['searchOption_entry'].set(settings.get('searchOption', 'differ'))

def browse_fileA(entries):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entries['fileA_entry'].delete(0, tk.END)
        entries['fileA_entry'].insert(0, file_path)

def browse_fileB(entries):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entries['fileB_entry'].delete(0, tk.END)
        entries['fileB_entry'].insert(0, file_path)

def browse_outputDir(entries):
    directory = filedialog.askdirectory()
    if directory:
        entries['outputDir_entry'].delete(0, tk.END)
        entries['outputDir_entry'].insert(0, directory)

def file_compare(fileA, fileB, searchOption):
    
    with open(fileA, 'r') as fa, open(fileB, 'r') as fb:
        lines_a = fa.readlines()
        lines_b = fb.readlines()
    
    if len(lines_a) >= len(lines_b):
        larger_list = lines_a
        smaller_list = lines_b
    else:
        larger_list = lines_b
        smaller_list = lines_a
    
    temp_list = larger_list.copy()
    matches = 0
    
    if searchOption == "differ":
        
        for line in smaller_list:
            if line in temp_list:
                temp_list.remove(line)
                
        for line in temp_list:
            matches += 1
    
    if searchOption == "match":
        
        for line in smaller_list:
            if line not in temp_list:
                temp_list.remove(line)
                
        for line in temp_list:
            matches += 1
            
    return temp_list, matches

def ensure_unique_outputName(name, dir):
    counter = 1
    outputName_real = os.path.join(dir, f"{name}{EXTENSION}")
    while os.path.exists(outputName_real):
        outputName_real = os.path.join(dir, f"{name}_{counter}{EXTENSION}")
        counter += 1
    return outputName_real

def compare_complete_message(matches, outputName_real):
    message = f"Operation Complete!\n\nNumber of matches found: {matches}\nOutput file written: {outputName_real}"
    messagebox.showinfo("Operation Complete", message)

def process(entries):
    
    fileA = entries['fileA_entry'].get()
    fileB = entries['fileB_entry'].get()
    searchOption = entries['searchOption_entry'].get()
    outputDir = entries['outputDir_entry'].get()
    outputName = entries['outputName_entry'].get()
    
    settings = {
        'fileA' : fileA,
        'fileB' : fileB,
        'searchOption' : searchOption,
        'outputDir' : outputDir,
        'outputName' : outputName
    }
    
    save_settings(settings)
    
    if not os.path.isfile(fileA) or not os.path.isfile(fileB):
        messagebox.showerror("Error", "Both input files must be valid text files.")
        return
    
    if not outputDir or not os.path.isdir(outputDir):
        messagebox.showerror("Error", "Please specify a valid output directory.")
        return
    
    if not outputName:
        outputName = "output"
    
    outputName_real = ensure_unique_outputName(outputName, outputDir)
    
    match_list, matches = file_compare(fileA, fileB, searchOption)
            
    with open(outputName_real, 'w') as f_out:
        f_out.writelines(match_list)
        
    compare_complete_message(matches, outputName_real)

Tk = tk.Tk()
Tk.title(TITLE)
Tk.geometry(GEOMETRY)
Tk.resizable(RESIZABLE, RESIZABLE)

create_widgets(Tk, load_settings())

Tk.mainloop()
