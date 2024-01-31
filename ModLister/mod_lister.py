import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def save_settings():
    settings = {
        "folder_path": folder_entry.get(),
        "extensions": extension_entry.get(),
        "smart_spacing": smart_spacing_var.get(),
        "include_extension": extension_var.get(),
        "include_subdirectories": subdirectories_var.get(),
        "output_path": output_path_entry.get(),
        "output_filename": output_filename_entry.get(),
        "exclude_numbers": numbers_var.get(),
        "exclude_letters": letters_var.get(),
        "exclude_symbols": symbols_var.get(),
        "advanced_inclusion": advanced_var.get(),
        "include_criteria": include_entry.get(),
        "exclude_criteria": exclude_entry.get(),
        "output_exclusion": output_exclusion_var.get(),
        "output_exclusion_text": output_exclusion_entry.get()
    }

    with open("settings.json", "w") as file:
        json.dump(settings, file)

def load_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)

        print("Loaded settings:", settings)

        # Clear entry fields before inserting loaded values
        folder_entry.delete(0, tk.END)
        extension_entry.delete(0, tk.END)
        output_path_entry.delete(0, tk.END)
        output_filename_entry.delete(0, tk.END)
        include_entry.delete(0, tk.END)
        exclude_entry.delete(0, tk.END)
        output_exclusion_entry.delete(0, tk.END)

        folder_entry.insert(tk.END, settings.get("folder_path", ""))
        extension_entry.insert(tk.END, settings.get("extensions", ""))
        smart_spacing_var.set(settings.get("smart_spacing", 0))
        extension_var.set(settings.get("include_extension", 0))
        subdirectories_var.set(settings.get("include_subdirectories", 0))
        output_path_entry.insert(tk.END, settings.get("output_path", ""))
        output_filename_entry.insert(tk.END, settings.get("output_filename", ""))
        numbers_var.set(settings.get("exclude_numbers", 0))
        letters_var.set(settings.get("exclude_letters", 0))
        symbols_var.set(settings.get("exclude_symbols", 0))
        advanced_var.set(settings.get("advanced_inclusion", 0))
        include_entry.insert(tk.END, settings.get("include_criteria", ""))
        exclude_entry.insert(tk.END, settings.get("exclude_criteria", ""))
        output_exclusion_var.set(settings.get("output_exclusion", 0))
        output_exclusion_entry.insert(tk.END, settings.get("output_exclusion_text", ""))
    except FileNotFoundError:
        print("Settings file not found.")
        pass

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)

def browse_output_path():
    output_path = filedialog.askdirectory()
    if output_path:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(tk.END, output_path)
        
def check_duplicates():
    # Get the specified text file path
    text_file_path = text_file_entry.get()

    # Check if the file exists
    if not os.path.isfile(text_file_path):
        messagebox.showerror("File Not Found", "The specified file does not exist.")
        return

    # Read the contents of the text file
    with open(text_file_path, "r") as file:
        lines = file.readlines()

    # Remove newline characters from the lines
    lines = [line.strip() for line in lines]

    # Find duplicate lines
    duplicates = []
    seen = set()
    for line in lines:
        if line in seen:
            duplicates.append(line)
        else:
            seen.add(line)

    # Handle duplicates
    handle_duplicates(duplicates)

def handle_duplicates(duplicate_lines):
    handled_duplicates = set()
    for line in duplicate_lines:
        if line in handled_duplicates:
            continue
        response = messagebox.askquestion("Duplicate Found", f"Duplicate line: {line}\n\nDo you want to remove it?")
        if response == "yes":
            handled_duplicates.add(line)

def remove_duplicate(file_path, duplicate):
    # Read the contents of the text file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Remove the duplicate line
    lines.remove(duplicate + "\n")

    # Write the updated contents back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

    # Show a confirmation message
    messagebox.showinfo("Duplicate Removed", "One instance of the duplicate has been removed from the file.")

def validate_checkboxes():
    if numbers_var.get() == 1:
        letters_var.set(0)
    elif letters_var.get() == 1:
        numbers_var.set(0)

def generate_file_list():
    
    save_settings()
    
    folder_path = folder_entry.get()
    extensions = extension_entry.get().replace(' ', '').split(',')
    smart_spacing = smart_spacing_var.get() == 1
    include_extension = extension_var.get() == 1
    include_subdirectories = subdirectories_var.get() == 1
    output_path = output_path_entry.get()
    output_filename = output_filename_entry.get().strip()
    exclude_numbers = numbers_var.get() == 1
    exclude_letters = letters_var.get() == 1
    exclude_symbols = symbols_var.get() == 1
    advanced_inclusion = advanced_var.get() == 1
    include_criteria = include_entry.get().strip().split(',')
    exclude_criteria = exclude_entry.get().strip().split(',')
    output_exclusion = output_exclusion_var.get() == 1
    output_exclusion_text = output_exclusion_entry.get().strip()

    # Extract strings from output_exclusion_text
    exclusion_list = [s.strip()[1:-1] for s in output_exclusion_text.split(',')]

    # Validate folder path
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    # Validate output path
    if not os.path.isdir(output_path):
        messagebox.showerror("Error", "Invalid output file path!")
        return

    # Search for files in the specified folder
    files = []
    file_extensions = []
    for root, dirs, filenames in os.walk(folder_path):
        if not include_subdirectories and root != folder_path:
            break
        for filename in filenames:
            file_ext = os.path.splitext(filename)[1]
            if file_ext.lower() in [ext.lower() for ext in extensions]:
                files.append(filename)
                file_extensions.append(file_ext)

    if not files:
        messagebox.showinfo("No Files Found", "No files found in the specified directory.")
        return

    # Generate output file name
    output_file_path = os.path.join(output_path, output_filename + ".txt")
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = os.path.join(output_path, output_filename + f"_{counter}.txt")
        counter += 1

    # Create the output text file
    with open(output_file_path, 'w') as file:
        filtered_files = []
        for filename, file_ext in zip(files, file_extensions):
            filtered_filename = os.path.splitext(filename)[0]
            if exclude_numbers:
                filtered_filename = ''.join(char for char in filtered_filename if not char.isdigit())
            if exclude_letters:
                filtered_filename = ''.join(char for char in filtered_filename if not char.isalpha())
            if exclude_symbols:
                filtered_filename = ''.join(char for char in filtered_filename if char.isalnum())
            if filtered_filename.endswith('v'):
                filtered_filename = filtered_filename[:-1]
            
            if smart_spacing:
                spaced_filename = ''
                for i, char in enumerate(filtered_filename):
                    if char.islower():
                        if i < len(filtered_filename) - 2:
                            if filtered_filename[i:i+3] == 'for':
                                spaced_filename += ' ' + char
                            else:
                                spaced_filename += char
                        else:
                            spaced_filename += char
                    elif char.isupper():
                        if i != 0 and not filtered_filename[i-1].isupper():
                            spaced_filename += ' ' + char
                        elif i < len(filtered_filename) - 1 and filtered_filename[i+1].islower():
                            spaced_filename += ' ' + char
                        else:
                            spaced_filename += char
                    else:
                        spaced_filename += char
                
                spaced_filename = spaced_filename.strip()

                if ' for' in spaced_filename:
                    index = spaced_filename.index(' for')
                    if index > 0 and spaced_filename[index-1].isupper() and spaced_filename[index-2] == ' ':
                        spaced_filename = spaced_filename[:index-2] + spaced_filename[index-1:]  # Remove the space before the capital letter

                filtered_filename = spaced_filename
            
            if include_extension and file_ext:
                filtered_filename += file_ext

            if output_exclusion and exclusion_list:
                for exclusion_string in exclusion_list:
                    filtered_filename = filtered_filename.replace(exclusion_string, '')
            
            filtered_files.append(filtered_filename)
        file.write('\n'.join(filtered_files))

    messagebox.showinfo("File List Generated", f"{len(files)} files found. Output file saved at:\n{output_file_path}")

# Create the main window
window = tk.Tk()
window.title("ModLister")
window.geometry("600x550")
window.resizable(False, False)

# Create a notebook (tabs container)
notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

# Build File tab
build_file_tab = ttk.Frame(notebook)
notebook.add(build_file_tab, text="Build File")

# Folder location
folder_label = tk.Label(build_file_tab, text="Folder Location:")
folder_label.pack()

folder_frame = tk.Frame(build_file_tab)
folder_frame.pack()

folder_entry = tk.Entry(folder_frame, width=50)
folder_entry.pack(side=tk.LEFT)

folder_browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
folder_browse_button.pack(side=tk.LEFT)

# File extension(s)
extension_label = tk.Label(build_file_tab, text="File Extension(s):")
extension_label.pack()

extension_entry = tk.Entry(build_file_tab, width=50)
extension_entry.insert(tk.END, ".*")
extension_entry.pack()

# Include or ignore subdirectories
subdirectories_var = tk.IntVar(value=0)
subdirectories_checkbutton = tk.Checkbutton(build_file_tab, text="Include Subdirectories", variable=subdirectories_var)
subdirectories_checkbutton.pack()

# Output file path
output_path_label = tk.Label(build_file_tab, text="Output File Path:")
output_path_label.pack()

output_path_frame = tk.Frame(build_file_tab)
output_path_frame.pack()

output_path_entry = tk.Entry(output_path_frame, width=50)
output_path_entry.pack(side=tk.LEFT)

output_path_browse_button = tk.Button(output_path_frame, text="Browse", command=browse_output_path)
output_path_browse_button.pack(side=tk.LEFT)

# Exclude numbers, letters, and symbols
exclude_frame = tk.LabelFrame(build_file_tab, text="Choose one or neither:")
exclude_frame.pack()

numbers_var = tk.IntVar(value=0)
numbers_checkbutton = tk.Checkbutton(exclude_frame, text="Exclude Numbers", variable=numbers_var,
                                     command=validate_checkboxes)
numbers_checkbutton.pack(side=tk.LEFT)

letters_var = tk.IntVar(value=0)
letters_checkbutton = tk.Checkbutton(exclude_frame, text="Exclude Letters", variable=letters_var,
                                    command=validate_checkboxes)
letters_checkbutton.pack(side=tk.LEFT)

symbols_var = tk.IntVar(value=0)
symbols_checkbutton = tk.Checkbutton(build_file_tab, text="Exclude Symbols", variable=symbols_var)
symbols_checkbutton.pack()

# Smart spacing function check box
smart_spacing_var = tk.IntVar(value=0)
smart_spacing_checkbutton = tk.Checkbutton(build_file_tab, text="Smart-Spacing", variable=smart_spacing_var)
smart_spacing_checkbutton.pack()

# Include file extensions in output file
extension_var = tk.IntVar(value=0)
extension_checkbutton = tk.Checkbutton(build_file_tab, text="Include File Extensions", variable=extension_var)
extension_checkbutton.pack()

# Output exclusion
output_exclusion_var = tk.IntVar(value=0)

def show_hide_output_exclusion():
    output_exclusion_frame.pack() if output_exclusion_var.get() == 1 else output_exclusion_frame.pack_forget()

output_exclusion_checkbutton = tk.Checkbutton(build_file_tab, text="Output Exclusion", variable=output_exclusion_var,
                                      command=show_hide_output_exclusion)
output_exclusion_checkbutton.pack()

output_exclusion_frame = tk.Frame(build_file_tab)

output_exclusion_label = tk.Label(output_exclusion_frame, text="Output Exclusion Text (\"a\", \"b\", etc):")
output_exclusion_label.pack()

output_exclusion_entry = tk.Entry(output_exclusion_frame, width=50)
output_exclusion_entry.pack()

show_hide_output_exclusion()

# Advanced inclusion/exclusion options
advanced_var = tk.IntVar(value=0)

def show_hide_advanced():
    advanced_frame.pack() if advanced_var.get() == 1 else advanced_frame.pack_forget()

advanced_checkbutton = tk.Checkbutton(build_file_tab, text="Advanced Inclusion/Exclusion", variable=advanced_var,
                                      command=show_hide_advanced)
advanced_checkbutton.pack()

advanced_frame = tk.Frame(build_file_tab)

include_label = tk.Label(advanced_frame, text="Include:")
include_label.pack()

include_entry = tk.Entry(advanced_frame, width=50)
include_entry.pack()

exclude_label = tk.Label(advanced_frame, text="Exclude:")
exclude_label.pack()

exclude_entry = tk.Entry(advanced_frame, width=50)
exclude_entry.pack()

show_hide_advanced()

# Output file name
output_filename_label = tk.Label(build_file_tab, text="Output File Name:")
output_filename_label.pack()

output_filename_entry = tk.Entry(build_file_tab, width=50)
output_filename_entry.insert(tk.END, "output")
output_filename_entry.pack()

# Generate file list button
generate_button = tk.Button(build_file_tab, text="Generate File List", command=generate_file_list)
generate_button.pack()

# Number of files found label
num_files_label = tk.Label(build_file_tab, text="")
num_files_label.pack()

# Actions tab
actions_tab = ttk.Frame(notebook)
notebook.add(actions_tab, text="Actions")

# Text box for specifying the text file
text_file_label = tk.Label(actions_tab, text="Text File:")
text_file_label.pack()

text_file_entry = tk.Entry(actions_tab, width=50)
text_file_entry.pack()

# Button for checking duplicates
check_duplicates_button = tk.Button(actions_tab, text="Check Duplicates", command=check_duplicates)
check_duplicates_button.pack()

load_settings()

window.mainloop()